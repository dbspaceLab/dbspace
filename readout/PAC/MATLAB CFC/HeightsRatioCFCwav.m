function MIs = HeightsRatioCFCwav(coefsForAmp,coefsForPhase,freqForAmp,freqForPhase,n,method,option)
%HEIGHTSRATIOCFCWAV Calculates and displays the CFC Comulolograms based on
%the Modulation Index/Ratio used in AM (Amplitude-Modulation) Radio 
%   MI = HeightsRatioCFCwav(oscAmpMod,oscForPhase,freqForAmp,freqForPhase,n,method,option)
%   coefsForAmp are wavelet coefficients at freqForAmp 
%   around freqForAmp with bandwidth specified by freqForPhase.
%   coefsForPhase are wavelet coefficients at freqForPhase
%   around freqForPhase with some small bandwidth
%   n is the number phasebins for the Heights-Ratio Modulation Index(MI)
%   method: there are 3 ways of doing this
%       1) 'Lakatos' -- h_max/h_min
%       2) 'Tort' -- (h_max - h_min)/h_max;
%       3) 'AM Radio' --- (h_max - h_min)/(h_max + h_min)
%   option: 'Yes' show comodulogram; 'No' don't show comodulogram
    
    % Applying Kullback-Leibler Divergence-based CFC to Oscillation Data
    phaseBins = -pi:(2*pi/n):pi; highFreqAmplitude = zeros(1,n);
    MIs = zeros(length(freqForPhase),length(freqForAmp));
    % Phases will change each row. Amplitudes will change each column
    for cc = 1:length(freqForAmp)
        for rr = 1:length(freqForPhase)
            amplitudes = abs(coefsForAmp(cc,:));
            phases = angle(coefsForPhase(rr,:));
            for kk = 1:n
                amps = amplitudes(phases > phaseBins(kk) & phases <= phaseBins(kk+1));
                highFreqAmplitude(kk) = mean(amps);
            end
            if strcmp(method,'AM Radio')
                MIs(rr,cc) = (max(highFreqAmplitude)-min(highFreqAmplitude))/...
                    (max(highFreqAmplitude)+min(highFreqAmplitude));
            elseif strcmp(method,'Tort')
                MIs(rr,cc) = (max(highFreqAmplitude)-min(highFreqAmplitude))/...
                    (max(highFreqAmplitude));
            elseif strcmp(method,'Lakatos')
                MIs(rr,cc) = (max(highFreqAmplitude))/(min(highFreqAmplitude));
            else
                error('inputarg:invalid','method can only be "Lakatos", "Tort", or "AM Radio"');
            end
            disp(['Completed: rr = ' num2str(rr) ', cc = ' num2str(cc)]);
        end
    end
    if strcmp(option,'Yes')
        imagesc(freqForPhase,freqForAmp,MIs'); set(gca,'YDir','normal');
        xlabel('Frequency for Phase'); ylabel('Frequency for Amplitude');
    end
end