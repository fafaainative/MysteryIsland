import unittest

from game.game import (
    collect_item,
    create_player,
    move_player,
    restore_beacon,
)


class TestMysteryIsland(unittest.TestCase):
    def setUp(self):
        self.player = create_player("Ada")

    def test_new_player_starts_at_beach_with_five_energy(self):
        self.assertEqual(self.player["location"], "Beach")
        self.assertEqual(self.player["energy"], 5)
        self.assertEqual(self.player["inventory"], [])

    def test_invalid_destination_does_not_change_state(self):
        before = self.player.copy()
        success, message = move_player(self.player, "Desert")
        self.assertFalse(success)
        self.assertEqual(self.player["location"], before["location"])
        self.assertEqual(self.player["energy"], before["energy"])

    def test_legal_move_costs_one_energy(self):
        success, _ = move_player(self.player, "Jungle")
        self.assertTrue(success)
        self.assertEqual(self.player["location"], "Jungle")
        self.assertEqual(self.player["energy"], 4)

    def test_cannot_move_directly_from_beach_to_cave(self):
        success, _ = move_player(self.player, "Cave")
        self.assertFalse(success)
        self.assertEqual(self.player["energy"], 5)

    def test_rope_can_only_be_collected_in_jungle_and_once(self):
        success, _ = move_player(self.player, "Jungle")
        self.assertTrue(success)
        success, _ = collect_item(self.player, "rope")
        self.assertTrue(success)
        success, _ = collect_item(self.player, "rope")
        self.assertFalse(success)
        self.assertEqual(self.player["inventory"].count("rope"), 1)

    def test_cannot_cross_bridge_without_rope(self):
        move_player(self.player, "Jungle")
        move_player(self.player, "Cave")
        success, _ = move_player(self.player, "Old Bridge")
        self.assertFalse(success)
        self.assertEqual(self.player["location"], "Cave")

    def test_lantern_can_be_collected_in_cave(self):
        move_player(self.player, "Jungle")
        collect_item(self.player, "rope")
        move_player(self.player, "Cave")
        success, _ = collect_item(self.player, "lantern")
        self.assertTrue(success)
        self.assertIn("lantern", self.player["inventory"])

    def test_beacon_cannot_be_restored_without_lantern(self):
        self.player["location"] = "Lighthouse"
        success, _ = restore_beacon(self.player)
        self.assertFalse(success)
        self.assertFalse(self.player["won"])

    def test_beacon_can_be_restored_with_lantern_at_lighthouse(self):
        self.player["location"] = "Lighthouse"
        self.player["inventory"].append("lantern")
        success, _ = restore_beacon(self.player)
        self.assertTrue(success)
        self.assertTrue(self.player["won"])
        self.assertTrue(self.player["game_over"])

    def test_energy_never_becomes_negative(self):
        self.player["energy"] = 1
        success, _ = move_player(self.player, "Jungle")
        self.assertTrue(success)
        self.assertEqual(self.player["energy"], 0)
        self.assertTrue(self.player["game_over"])


if __name__ == "__main__":
    unittest.main()
