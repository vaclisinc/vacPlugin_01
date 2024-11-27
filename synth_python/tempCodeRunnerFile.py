def apply_adsr(data, sample_rate, attack, decay, sustain, release):
    total_samples = len(data)
    attack_samples = int(sample_rate * attack)
    decay_samples = int(sample_rate * decay)
    release_samples = int(sample_rate * release)
    sustain_samples = total_samples - attack_samples - decay_samples - release_samples

    envelope = np.zeros(total_samples)
    # Attack
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    # Decay
    envelope[attack_samples:attack_samples + decay_samples] = np.linspace(1, sustain, decay_samples)
    # Sustain
    envelope[attack_samples + decay_samples:attack_samples + decay_samples + sustain_samples] = sustain
    # Release
    envelope[-release_samples:] = np.linspace(sustain, 0, release_samples)

    return data * envelope