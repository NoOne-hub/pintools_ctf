/*
 * Copyright 2002-2019 Intel Corporation.
 * 
 * This software is provided to you as Sample Source Code as defined in the accompanying
 * End User License Agreement for the Intel(R) Software Development Products ("Agreement")
 * section 1.L.
 * 
 * This software and the related documents are provided as is, with no express or implied
 * warranties, other than those that are expressly stated in the License.
 */

#include <iostream>
#include <fstream>
#include "pin.H"
using std::cerr;
using std::ofstream;
using std::ios;
using std::string;
using std::endl;
using std::cout;

ofstream OutFile;

// The running count of instructions is kept here
// make it static to help the compiler optimize docount
static UINT64 icount = 0;
KNOB<string> KnobOutputFile(KNOB_MODE_WRITEONCE, "pintool",
    "a", "0", "specify output file name");

static long long int target_addr= 0;

// This function is called before every instruction is executed
VOID docount(void *ip) { 
    icount++; 
}
    
// Pin calls this function every time a new instruction is encountered
VOID Instruction(INS ins, VOID *v)
{
    // Insert a call to docount before every instruction, no arguments are passed
    long long int addr = (long long int)INS_Address(ins);
    if((addr >> 44 & 0xf)== 0x7 || (addr >> 28 & 0xf) == 0xf)
        return;
    
    INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)docount, IARG_END);
}

VOID Instruction_TARGET(INS ins, VOID *v)
{
    // Insert a call to docount before every instruction, no arguments are passed
    long long int addr = (long long int)INS_Address(ins);
    if((addr >> 44 & 0xf)== 0x7 || (addr >> 28 & 0xf) == 0xf)
        return;
    if(addr == target_addr)
        INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)docount, IARG_END);
}


VOID Instruction_TARGET_PIE(INS ins, VOID *v)
{
    // Insert a call to docount before every instruction, no arguments are passed
    long long int addr = (long long int)INS_Address(ins);
    if((addr >> 44 & 0xf)== 0x7 || (addr >> 28 & 0xf) == 0xf)
        return;
    if( (addr&0xFFF) == target_addr)
        INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)docount, IARG_END);
}


// This function is called when the application exits
VOID Fini(INT32 code, VOID *v)
{
    // Write to a file since cout and cerr maybe closed by the application
    // OutFile.setf(ios::showbase);
    // OutFile << KnobOutputFile.Value().c_str() << ":" << icount << endl;
    // OutFile.close();
    cout << "Count" << ":" << icount << endl;
    
}

/* ===================================================================== */
/* Print Help Message                                                    */
/* ===================================================================== */

INT32 Usage()
{
    cerr << "This tool counts the number of dynamic instructions executed" << endl;
    cerr << endl << KNOB_BASE::StringKnobSummary() << endl;
    return -1;
}

/* ===================================================================== */
/* Main                                                                  */
/* ===================================================================== */
/*   argc, argv are the entire command line: pin -t <toolname> -- ...    */
/* ===================================================================== */

int main(int argc, char * argv[])
{
    // Initialize pin
    if (PIN_Init(argc, argv)) return Usage();

    //OutFile.open("inscount0.out",ios::app);

    target_addr = atoll(KnobOutputFile.Value().c_str());
    if(target_addr == 0)
        INS_AddInstrumentFunction(Instruction, 0);
    else if(target_addr <= 0xFFF)
        INS_AddInstrumentFunction(Instruction_TARGET_PIE, 0);
    else
        INS_AddInstrumentFunction(Instruction_TARGET, 0);

    // Register Fini to be called when the application exits
    PIN_AddFiniFunction(Fini, 0);
    
    // Start the program, never returns
    PIN_StartProgram();
    
    return 0;
}
