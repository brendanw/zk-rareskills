// SPDX-License-Identifier: MIT
pragma solidity 0.8.25;

contract Problem1 {

    struct ECPoint {
	    uint256 x;
	    uint256 y;
    }

    function rationalAdd(ECPoint calldata A, ECPoint calldata B, uint256 num, uint256 den) public view returns (bool verified) {
	    // return true if the prover knows two numbers that add up to num/den

        // got curve_order from py_ecc.bn128
        uint256 curve_order = 21888242871839275222246405745257275088548364400416034343698204186575808495617;

        // got generator point from py_ecc.bn128 as well
        uint256 gx = 1;
        uint256 gy = 2;

        // a + b = c where a, b, and c are rational numbers
        // A = aG
        // B = bG
        // C = cG
        // c = num / den
        // aG + bG = (num/den)*G
        // A + B = (num/den)*G

        // I need to add two elliptic curve points A and B in solidity
        // elliptic curve addition is static call to address(6)
        (bool ok, bytes memory CResult) = address(6).staticcall(abi.encode(A.x, A.y, B.x, B.y));
        require(ok, "failed ec addition");
        (uint256 CX, uint256 CY) = abi.decode(CResult, (uint256, uint256));

        // I need to take the inverse of (den * G) and then multiply that by (num * G)
        uint256 invDen = cleanModExp(den, curve_order - 2, curve_order);
        uint256 c = num * invDen;

        // need to get cG using elliptic curve multiplication
        (bool ok2, bytes memory ecProduct) = address(7).staticcall(abi.encode(gx, gy, c));
        require(ok2, "mul ec failed");
        (uint256 productX, uint256 productY) = abi.decode(ecProduct, (uint256, uint256));

        verified = (productX == CX && productY == CY);
    }

    function cleanModExp(uint256 base, uint256 exponent, uint256 modulus) public view returns (uint256) {
        bytes memory baseBytes = uint256ToBytes(base);
        bytes memory exponentBytes = uint256ToBytes(exponent);
        bytes memory modulusBytes = uint256ToBytes(modulus);

        bytes memory resultBytes = modExp(baseBytes, exponentBytes, modulusBytes);

        uint256 result;
        assembly {
            result := mload(add(resultBytes, 32))
        }

        return result;
    }

    function modExp(bytes memory base, bytes memory exponent, bytes memory modulus) public view returns (bytes memory) {
        // Constructing the input data for the precompile
        uint256 baseLen = base.length;
        uint256 expLen = exponent.length;
        uint256 modLen = modulus.length;

        bytes memory input = abi.encodePacked(uint256ToBytes(baseLen), uint256ToBytes(expLen), uint256ToBytes(modLen), base, exponent, modulus);

        // Prepare output buffer
        bytes memory output = new bytes(modLen);

        // Call the precompile using Solidity's low-level call
        (bool success, bytes memory result) = address(0x05).staticcall(input);

        require(success, "Modular exponentiation failed");
        return result;
    }

    function uint256ToBytes(uint256 x) internal pure returns (bytes memory) {
        bytes memory b = new bytes(32);
        assembly { mstore(add(b, 32), x) }
        return b;
    }
}