OPENQASM 2.0;
include "qelib1.inc";
qreg qubits[19];
h qubits[18];
h qubits[18];
ccx qubits[9],qubits[17],qubits[18];
h qubits[18];
h qubits[17];
h qubits[17];
ccx qubits[8],qubits[16],qubits[17];
h qubits[17];
h qubits[16];
h qubits[16];
ccx qubits[7],qubits[15],qubits[16];
h qubits[16];
h qubits[15];
h qubits[15];
ccx qubits[6],qubits[14],qubits[15];
h qubits[15];
h qubits[14];
h qubits[14];
ccx qubits[5],qubits[13],qubits[14];
h qubits[14];
h qubits[13];
h qubits[13];
ccx qubits[4],qubits[12],qubits[13];
h qubits[13];
h qubits[12];
h qubits[12];
ccx qubits[3],qubits[11],qubits[12];
h qubits[12];
h qubits[11];
h qubits[11];
ccx qubits[2],qubits[10],qubits[11];
h qubits[11];
h qubits[10];
h qubits[10];
ccx qubits[0],qubits[1],qubits[10];
h qubits[10];
h qubits[10];
h qubits[11];
ccx qubits[2],qubits[10],qubits[11];
h qubits[11];
h qubits[11];
h qubits[12];
ccx qubits[3],qubits[11],qubits[12];
h qubits[12];
h qubits[12];
h qubits[13];
ccx qubits[4],qubits[12],qubits[13];
h qubits[13];
h qubits[13];
h qubits[14];
ccx qubits[5],qubits[13],qubits[14];
h qubits[14];
h qubits[14];
h qubits[15];
ccx qubits[6],qubits[14],qubits[15];
h qubits[15];
h qubits[15];
h qubits[16];
ccx qubits[7],qubits[15],qubits[16];
h qubits[16];
h qubits[16];
h qubits[17];
ccx qubits[8],qubits[16],qubits[17];
h qubits[17];
h qubits[17];
h qubits[18];
ccx qubits[9],qubits[17],qubits[18];
h qubits[18];
h qubits[18];
h qubits[17];
h qubits[17];
ccx qubits[8],qubits[16],qubits[17];
h qubits[17];
h qubits[16];
h qubits[16];
ccx qubits[7],qubits[15],qubits[16];
h qubits[16];
h qubits[15];
h qubits[15];
ccx qubits[6],qubits[14],qubits[15];
h qubits[15];
h qubits[14];
h qubits[14];
ccx qubits[5],qubits[13],qubits[14];
h qubits[14];
h qubits[13];
h qubits[13];
ccx qubits[4],qubits[12],qubits[13];
h qubits[13];
h qubits[12];
h qubits[12];
ccx qubits[3],qubits[11],qubits[12];
h qubits[12];
h qubits[11];
h qubits[11];
ccx qubits[2],qubits[10],qubits[11];
h qubits[11];
h qubits[10];
h qubits[10];
ccx qubits[0],qubits[1],qubits[10];
h qubits[10];
h qubits[10];
h qubits[11];
ccx qubits[2],qubits[10],qubits[11];
h qubits[11];
h qubits[11];
h qubits[12];
ccx qubits[3],qubits[11],qubits[12];
h qubits[12];
h qubits[12];
h qubits[13];
ccx qubits[4],qubits[12],qubits[13];
h qubits[13];
h qubits[13];
h qubits[14];
ccx qubits[5],qubits[13],qubits[14];
h qubits[14];
h qubits[14];
h qubits[15];
ccx qubits[6],qubits[14],qubits[15];
h qubits[15];
h qubits[15];
h qubits[16];
ccx qubits[7],qubits[15],qubits[16];
h qubits[16];
h qubits[16];
h qubits[17];
ccx qubits[8],qubits[16],qubits[17];
h qubits[17];
h qubits[17];
