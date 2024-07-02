pragma circom 2.1.3;

include "comparators.circom";

template TimestampsBetween() {
    signal input sourceTimestamps[2];
    signal input testedTimestamps[2];

    signal output out;

    // Make sure source0 <= source1
    component lteSource = LessEqThan(64);
    lteSource.in[0] <== sourceTimestamps[0];
    lteSource.in[1] <== sourceTimestamps[1];
    lteSource.out === 1;

    // Make sure tested0 <= tested1
    component lteTested = LessEqThan(64);
    lteTested.in[0] <== testedTimestamps[0];
    lteTested.in[1] <== testedTimestamps[1];
    lteTested.out === 1;

    // tested0 >= source0
    component gteFrom = GreaterEqThan(64);
    gteFrom.in[0] <== testedTimestamps[0];
    gteFrom.in[1] <== sourceTimestamps[0];
    gteFrom.out === 1;

    // tested1 <= source1
    component lteTo = LessEqThan(64);
    lteTo.in[0] <== testedTimestamps[1];
    lteTo.in[1] <== sourceTimestamps[1];
    lteTo.out === 1;

    out <== (lteSource.out + lteTested.out + gteFrom.out + lteTo.out) * 1/4;
}

component main {public [testedTimestamps]} = TimestampsBetween();