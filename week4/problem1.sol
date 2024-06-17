// SPDX-License-Identifier: MIT
pragma solidity 0.8.25;

contract PairingHomework {

    struct G1Point {
        uint256 x;
        uint256 y;
    }

    // Encoding of field elements is: X[0] * z + X[1]
    struct G2Point {
        uint256[2] x;
        uint256[2] y;
    }

    // greek letters confuse me, so I've replaced them with normal letters such that we
    // are validating
    // 0 = e(-A1,B2) + e(D1, H2) + e(X1, Y2) + e(C1,J2)
    // where X1 = x1 + x2 + x3
    // AND
    // A1 = a*G1
    // B2 = b*G2
    // D1 = d*G1
    // H2 = h*G2
    // X1 = (x1 + x2 + x3) * G1
    // Y2 = y*G2
    // C1 = c*G1
    // J2 = j*J2
    // alternatively we can thus write
    // 0 = -a*b + d*h + (x1+x2+x3)*y + c*j OR ab = dh + (x1+x2+x3)*y + c*j
    function verifyComputation(
        uint256 x1,
        uint256 x2,
        uint256 x3,
        G1Point calldata A1,
        G2Point calldata B2,
        G1Point calldata C1
    ) public view returns (bool) {
        // Use the ethereum precompiles for addition and multiplication to compute X

        // Then the precompile for pairing to compute the entire equation in one go.

    }

    /* @return The result of computing the pairing check
   *         e(p1[0], p2[0]) *  .... * e(p1[n], p2[n]) == 1
   *         For example,
   *         pairing([P1(), P1().negate()], [P2(), P2()]) should return true.
   */
    function pairing(
        G1Point memory a1,
        G2Point memory a2,
        G1Point memory b1,
        G2Point memory b2,
        G1Point memory c1,
        G2Point memory c2,
        G1Point memory d1,
        G2Point memory d2
    ) internal view returns (bool) {
        G1Point[4] memory p1 = [a1, b1, c1, d1];
        G2Point[4] memory p2 = [a2, b2, c2, d2];

        uint256 inputSize = 24;
        uint256[] memory input = new uint256[](inputSize);

        for (uint256 i = 0; i < 4; i++) {
            uint256 j = i * 6;
            input[j + 0] = p1[i].X;
            input[j + 1] = p1[i].Y;
            input[j + 2] = p2[i].X[0];
            input[j + 3] = p2[i].X[1];
            input[j + 4] = p2[i].Y[0];
            input[j + 5] = p2[i].Y[1];
        }

        uint256[1] memory out;
        bool success;

        // solium-disable-next-line security/no-inline-assembly
        assembly {
            success := staticcall(sub(gas(), 2000), 8, add(input, 0x20), mul(inputSize, 0x20), out, 0x20)
        // Use "invalid" to make gas estimation work
            switch success case 0 {invalid()}
        }

        require(success, "pairing-opcode-failed");

        return out[0] != 0;
    }

    /**
    * From tornado cash contract https://github.com/tornadocash/tornado-core/blob/master/contracts/Verifier.sol#L100
    */
    function scalar_mul(G1Point memory p, uint256 s) internal view returns (G1Point memory r) {
        uint256[3] memory input;
        input[0] = p.x;
        input[1] = p.y;
        input[2] = s;
        bool success;
        // solium-disable-next-line security/no-inline-assembly
        assembly {
            success := staticcall(sub(gas(), 2000), 7, input, 0x80, r, 0x60)
        // Use "invalid" to make gas estimation work
            switch success case 0 {invalid()}
        }

        require(success, "pairing-mul-failed");
    }

    /*
    * @return r the sum of two points of G1
    * From tornado cash https://github.com/tornadocash/tornado-core/blob/master/contracts/Verifier.sol#L79
    */
    function plus(
        G1Point memory p1,
        G1Point memory p2
    ) internal view returns (G1Point memory r) {
        uint256[4] memory input;
        input[0] = p1.x;
        input[1] = p1.y;
        input[2] = p2.x;
        input[3] = p2.y;
        bool success;

        // solium-disable-next-line security/no-inline-assembly
        assembly {
            success := staticcall(sub(gas(), 2000), 6, input, 0xc0, r, 0x60)
        // Use "invalid" to make gas estimation work
            switch success case 0 {invalid()}
        }

        require(success, "pairing-add-failed");
    }
}