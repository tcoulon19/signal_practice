#Coulon Signal Project

import numpy as np
import matplotlib.pyplot as plt

#generate_wave takes in a sampling frequency, time duration, and wave frequency, and target SNR in dB and outputs values for time (time_range) 
#and sampled signal amplidude (sampled_wave) for a sine wave which can be plotted with matplotlib.
def generate_wave(sampling_frequency, time_duration, wave_frequency, snr_dB):

    time_step = 1 / sampling_frequency
    time_range = np.arange(0, time_duration, time_step)
    sampled_wave = np.sin(2 * np.pi * wave_frequency * time_range)
    sampled_wave = add_noise(sampled_wave, snr_dB)

    return (time_range, sampled_wave)

#add_noise takes in a clean signal and target SNR (dB) and outputs a signal with noise added
def add_noise(signal, snr_dB):

    snr = 10 ** (snr_dB / 10)
    noise = np.random.randn(len(signal))
    sum_signal_squared = np.sum(signal ** 2)
    sum_noise_squared = np.sum(noise ** 2)
    alpha = np.sqrt(sum_signal_squared / (snr * sum_noise_squared)) #alpha amplifies noise to meet SNR requirement
    signal_with_noise = signal + alpha * noise

    return signal_with_noise

#calculate_PSD takes in the sampled signal from generate_wave, the sampling frequency, and time duration, and outputs values of
#PSD (PSD_values) and frequency (frequencies_to_plot) to be plotted in the PSD.
def calculate_PSD(sampled_wave, sampling_frequency, time_duration):

    fft_size = int(sampling_frequency * time_duration) #Use sample length for fft
    dft = np.fft.fft(sampled_wave, fft_size)
    dft = np.fft.fftshift(dft)
    PSD_values = (abs(dft) ** 2) / fft_size #Square dft magnitude to get PSD and normalize by sample length

    frequency_resolution = sampling_frequency / fft_size
    frequencies_to_plot = np.arange(-(fft_size * frequency_resolution) // 2, (fft_size * frequency_resolution) // 2, \
        frequency_resolution)

    return (PSD_values, frequencies_to_plot)


#Inputs
sampling_frequency = 200000 #Hz
time_duration = .01 #s
wave_frequency = 1000 #Hz
snr_dB_1 = 20 #dB
snr_dB_2 = 5 #dB


#Plot signal and PSD for snr_dB_1
(time_range_1, sampled_wave_1) = generate_wave(sampling_frequency, time_duration, wave_frequency, snr_dB_1)
(PSD_values_1, frequencies_to_plot_1) = calculate_PSD(sampled_wave_1, sampling_frequency, time_duration)

plt.figure(0)
plt.plot(time_range_1, sampled_wave_1)
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.title("Voltage vs. Time, SNR = 20 dB")
plt.savefig("sine_wave_snr_20dB.png")

plt.figure(1)
plt.plot(frequencies_to_plot_1, 10 * np.log10(PSD_values_1))
plt.xlabel("Frequency (Hz)")
plt.ylabel("PSD (dB/Hz)")
plt.title("Power Spectral Density, SNR = 20 dB")
plt.savefig("PSD_snr_20dB.png")


#Plot signal and PSD for snr_dB_2
(time_range_2, sampled_wave_2) = generate_wave(sampling_frequency, time_duration, wave_frequency, snr_dB_2)
(PSD_values_2, frequencies_to_plot_2) = calculate_PSD(sampled_wave_2, sampling_frequency, time_duration)

plt.figure(2)
plt.plot(time_range_2, sampled_wave_2)
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.title("Voltage vs. Time, SNR = 5 dB")
plt.savefig("sine_wave_snr_5dB.png")

plt.figure(3)
plt.plot(frequencies_to_plot_2, 10 * np.log10(PSD_values_2))
plt.xlabel("Frequency (Hz)")
plt.ylabel("PSD (dB/Hz)")
plt.title("Power Spectral Density, SNR = 5 dB")
plt.savefig("PSD_snr_5dB.png")
