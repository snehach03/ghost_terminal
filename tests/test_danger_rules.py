import unittest
from ghost.danger_rules import check_command_danger

class TestDangerRules(unittest.TestCase):
    def test_fork_bomb(self): self.assertTrue(check_command_danger(":(){ :|:& };:")[0])
    def test_rm_rf(self): self.assertTrue(check_command_danger("rm -rf /")[0])
    def test_rm_safe(self): self.assertFalse(check_command_danger("rm note.txt")[0])
    def test_git_hard(self): self.assertTrue(check_command_danger("git reset --hard")[0])
    def test_git_soft(self): self.assertFalse(check_command_danger("git reset --soft")[0])
    def test_chmod(self): self.assertTrue(check_command_danger("chmod -R 777 .")[0])
if __name__ == "__main__": unittest.main()
