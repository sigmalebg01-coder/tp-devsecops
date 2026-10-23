from aiops.sanitize import bound_logs, mask_secrets


def test_masks_tokens_and_passwords():
    fake = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
    out = mask_secrets(f'token={fake} password: "hunter2" user=a.b@corp.fr')
    assert fake not in out and "hunter2" not in out and "a.b@corp.fr" not in out


def test_bounds_volume():
    lines = [f"line {i} " + "x" * 400 for i in range(1000)]
    kept = bound_logs(lines, max_lines=50, max_chars=2000)
    assert len(kept) <= 50 and sum(len(k) for k in kept) <= 2000
    assert kept[-1].startswith("line 999")