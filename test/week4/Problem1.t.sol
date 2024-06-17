// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {PairingHomework} from "../../src/week4/Problem1.sol";

contract PairingHomeworkTest is Test {
    PairingHomework public pairingHomework;

    function setUp() public {
        pairingHomework = new PairingHomework();
    }

    function test_correctSolution() public {
        bool result = pairingHomework.verifyComputation(
            1, // x1
            2, // x2
            3, // x3
            // A1
            PairingHomework.G1Point({ x: 1368015179489954701390400359078579693043519447331113978918064868415326638035, y: 9918110051302171585080402603319702774565515993150576347155970296011118125764 }),
            // B2
            PairingHomework.G2Point(
                {
                    x: [7883069657575422103991939149663123175414599384626279795595310520790051448551, 8346649071297262948544714173736482699128410021416543801035997871711276407441],
                    y: [3343323372806643151863786479815504460125163176086666838570580800830972412274, 16795962876692295166012804782785252840345796645199573986777498170046508450267]
                }
            ),
            // C1
            PairingHomework.G1Point(
                {
                    x: 3353031288059533942658390886683067124040920775575537747144343083137631628272,
                    y: 19321533766552368860946552437480515441416830039777911637913418824951667761761
                }
            )
        );

        assertEq(result, true);
    }

    function test_incorrectSolution() public {
        bool result = pairingHomework.verifyComputation(
            1, // x1
            1, // x2
            1, // x3
            // A1
            PairingHomework.G1Point({ x: uint256(0), y: uint256(0) }),
            // B2
            PairingHomework.G2Point(
                {
                    x: [uint256(0), uint256(0)],
                    y: [uint256(0), uint256(0)]
                }
            ),
            // C1
            PairingHomework.G1Point(
                {
                    x: uint256(0),
                    y: uint256(0)
                }
            )
        );

        assertEq(result, false);
    }


}
