// SPDX-License-Identifier: MIT
pragma solidity 0.8.25;

contract Problem2 {
    struct ECPoint {
	    uint256 x;
	    uint256 y;
    }

    function matmul(uint256[] calldata matrix,
                uint256 n, // n x n for the matrix
                ECPoint[] calldata s, // n elements
                uint256[] calldata o // n elements
               ) public view returns (bool) {
        // revert if dimensions don't make sense or the matrices are empty
        require(matrix.length == n * n, "Matrix length does not match n * n");
        require(s.length == n, "Length of s does not match n");
        require(o.length == n, "Length of o does not match n");

        // got generator point from py_ecc.bn128
        ECPoint memory G = ECPoint({x: 1, y: 2});

        // compare lefthand vs right for each row of vectors
        for (uint256 i = 0; i < n; i++) {
            // compute lefthand side
            ECPoint memory lefthand = ECPoint({x: 0, y: 0});
            for (uint256 j = 0; j < n; j++) {
                uint256 matrixElem = matrix[i*n + j];
                ECPoint memory resultElem = scalar_mul(s[j], matrixElem);
                lefthand = plus(resultElem, lefthand);
            }

            // compute righthand side. will need to
            ECPoint memory right = scalar_mul(G, o[i]);

            // if lefthand and righthand side do not match, return early
            if (lefthand.x != right.x || lefthand.y != right.y) {
                return false;
            }
        }

	    // return true if Ms == o elementwise. You need to do n equality checks.
        // If you're lazy, you can hardcode n to 3, but it is suggested that you do this with a for loop
        return true;
    }

    /**
    * From tornado cash contract https://github.com/tornadocash/tornado-core/blob/master/contracts/Verifier.sol#L100
    */
    function scalar_mul(ECPoint memory p, uint256 s) internal view returns (ECPoint memory r) {
        uint256[3] memory input;
        input[0] = p.x;
        input[1] = p.y;
        input[2] = s;
        bool success;
        // solium-disable-next-line security/no-inline-assembly
        assembly {
            success := staticcall(sub(gas(), 2000), 7, input, 0x80, r, 0x60)
            // Use "invalid" to make gas estimation work
            switch success case 0 { invalid() }
        }

        require(success, "pairing-mul-failed");
    }

    /*
    * @return r the sum of two points of G1
    * From tornado cash https://github.com/tornadocash/tornado-core/blob/master/contracts/Verifier.sol#L79
    */
    function plus(
        ECPoint memory p1,
        ECPoint memory p2
    ) internal view returns (ECPoint memory r) {
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
            switch success case 0 { invalid() }
        }

        require(success, "pairing-add-failed");
    }

}