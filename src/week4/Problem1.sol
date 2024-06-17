// SPDX-License-Identifier: MIT
pragma solidity 0.8.25;

import "forge-std/Test.sol";

contract PairingHomework {
    uint256 constant SNARK_SCALAR_FIELD = 21888242871839275222246405745257275088548364400416034343698204186575808495617;
    uint256 constant PRIME_Q = 21888242871839275222246405745257275088696311157297823662689037894645226208583;

    struct G1Point {
        uint256 x;
        uint256 y;
    }

    // Encoding of field elements is: X[0] * z + X[1]
    struct G2Point {
        uint256[2] x;
        uint256[2] y;
    }

    function testPairing() public view returns (bool) {
        G1Point memory G1 = G1Point({x: 1, y: 2});
        G2Point memory G2 = G2Point({
            x: [10857046999023057135944570762232829481370756359578518086990519993285655852781, 11559732032986387107991004021392285783925812861821192530917403151452391805634],
            y: [8495653923123431417604973247489272438418190587263600148770280649306958101930, 4082367875863433681332203403145435568316851327593401208105741076214120093531]
        });

        return pairing(
            G1,
            G2,
            G1,
            G2,
            G1,
            G2,
            G1,
            G2
        );
    }

    // greek letters confuse me, so I've replaced them with normal letters such that we
    // are validating
    // 0 = e(-A1,B2) + e(D1, H2) + e(X1, Y2) + e(C1,J2)
    //
    // where X1 = x1 + x2 + x3
    //
    // AND
    //
    // A1 = a*G1
    // B2 = b*G2
    // D1 = d*G1
    // H2 = h*G2
    // X1 = (x1 + x2 + x3) * G1
    // Y2 = y*G2
    // C1 = c*G1
    // J2 = j*J2
    //
    // alternatively we can thus write
    //
    // 0 = -a*b + d*h + (x1+x2+x3)*y + c*j OR ab = dh + (x1+x2+x3)*y + c*j
    //
    // caller passes in A1, B2, C1, and thus defines a, b, c, x1, x2, x3
    // thus we must pre-define/hardcode d, h, y, and j
    //
    // this function assumes
    // d=5 D1=5*G1
    // h=12 H2=12*G2
    // y=3 Y2=3*G2
    // j=2 J2=2*G2
    //
    // thus a valid solution is:
    // x1=1,x2=2,x3=3 where X1=6
    // a=2 A1=2*G1
    // b=42 B2=42*G2
    // c=3 C1=3*G1

    function verifyComputation(
        uint256 x1,
        uint256 x2,
        uint256 x3,
        G1Point calldata A1,
        G2Point calldata B2,
        G1Point calldata C1
    ) public view returns (bool) {
        G1Point memory G1 = G1Point({x: 1, y: 2});

        // Use the ethereum precompiles for addition and multiplication to compute X
        G1Point memory X1 = scalar_mul(G1, x1 + x2 + x3);

        // Calculate other points
        G1Point memory D1 = G1Point(
            {
                x: uint256(10744596414106452074759370245733544594153395043370666422502510773307029471145),
                y: uint256(848677436511517736191562425154572367705380862894644942948681172815252343932)
            }
        );

        G2Point memory H2 = G2Point(
            {
                x: [uint256(4351401811647638138392695977895401859084096897123577305203754529537814663109), uint256(2046729899889901964437012741252570163462327955511008570480857952505584629957)],
                y: [uint256(322506915963699862059245473966830598387691259163658767351233132602858049743), uint256(14316075702276096164483565793667862351398527813470041574939773541551376891710)]
            }
        );

        G2Point memory Y2 = G2Point(
            {
                x: [uint256(2725019753478801796453339367788033689375851816420509565303521482350756874229), uint256(7273165102799931111715871471550377909735733521218303035754523677688038059653)],
                y: [uint256(2512659008974376214222774206987427162027254181373325676825515531566330959255), uint256(957874124722006818841961785324909313781880061366718538693995380805373202866)]
            }
        );

        G2Point memory J2 = G2Point(
            {
                x: [uint256(18029695676650738226693292988307914797657423701064905010927197838374790804409), uint256(14583779054894525174450323658765874724019480979794335525732096752006891875705)],
                y: [uint256(2140229616977736810657479771656733941598412651537078903776637920509952744750), uint256(11474861747383700316476719153975578001603231366361248090558603872215261634898)]
            }
        );

        G1Point memory negA1 = negate(A1);

        // Then the precompile for pairing to compute the entire equation in one go.
        return pairing(
            negA1,
            B2,
            D1,
            H2,
            X1,
            Y2,
            C1,
            J2
        );
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
            input[j + 0] = p1[i].x;
            input[j + 1] = p1[i].y;
            input[j + 2] = p2[i].x[1];
            input[j + 3] = p2[i].x[0];
            input[j + 4] = p2[i].y[1];
            input[j + 5] = p2[i].y[0];
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

    /*
     * @return The negation of p, i.e. p.plus(p.negate()) should be zero.
    */
    function negate(G1Point memory p) internal pure returns (G1Point memory) {
        // The prime q in the base field F_q for G1
        if (p.x == 0 && p.y == 0) {
            return G1Point(0, 0);
        } else {
            return G1Point(p.x, PRIME_Q - (p.y % PRIME_Q));
        }
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