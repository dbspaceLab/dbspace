function MIs = NESCcomodulogram(sigForAmp,sigForPhase,freqForAmp,freqForPhase,fs,bw,passbandRipl,option)
%NESCCOMODULOGRAM Generates a Normalized-Envelope-to-Signal-Correlation Based Comodulogram
%   USAGE: MIs = ESCcomodulogram(sigForAmp,sigForPhase,freqForAmp,freqForPhase,fs,bw,passbandRipl,option)
%   sigForAmp is the input LFP to be analyzed for amplitude
%   sigForPhase is the input LFP to be analyzed for phase
%   freqForAmp is a vector of center frequencies (frequency for amplitude)
%   freqForPhase is a vector of frequency for phase controlling bandwidth
%   fs is sampling rate (Hz), bw is the bandwidth of the bandpass filters typically (4.5 Hz)
%   passbandRipl is on a linear scale (not decibel): its preferred value is 0.02
%   option: 'Yes' show comodulogram; 'No' don't show comodulogram

    oscAmpMod = CFCfilt(sigForAmp,freqForAmp,freqForPhase,fs,passbandRipl);
    oscForPhase = CFCfilt(sigForPhase,freqForPhase,bw,fs,passbandRipl);
    ModCorr = NormEnvSigCorrCFC(oscAmpMod,oscForPhase,freqForAmp,freqForPhase);
    MIs = atanh(abs(ModCorr));
    
    if strcmp(option,'Yes')
        imagesc(freqForPhase,freqForAmp,MIs'); set(gca,'YDir','normal');
        xlabel('Frequency for Phase'); ylabel('Frequency for Amplitude');
    end
end