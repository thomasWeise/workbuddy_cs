import Mathlib

theorem one_add_le_exp_real (x : ℝ) : 1 + x ≤ Real.exp x := by
  simpa [add_comm] using Real.add_one_le_exp x
