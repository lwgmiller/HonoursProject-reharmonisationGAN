
class Evaluate():

    def __init__(self, path: str):

        self.piece_signature_vector = []


        trk = music21.converter.parse(path)

        maxRange, minRange, meanRange, stdRange = self.Pitch_Range_Descriptors(trk)

        maxIntvl, minIntvl, meanIntvl, stdIntvl = self.Pitch_Interval_Range(trk)
        
        MaxDur, minDur, meanDur, stdDur = self.Note_Duration(trk)


        self.piece_signature_vector.extend(
            [self.Number_of_notes(trk)[1], 
            self.Occupation_Rate(trk),
            self.Polyphonic_Rate(trk),
            maxRange, minRange, meanRange, stdRange,
            maxIntvl, minIntvl, meanIntvl, stdIntvl,
            MaxDur, minDur, meanDur, stdDur
            ])
        



    def Number_of_notes(self, trk: stream):

        count = len(trk.recurse().notes)


        return count, count / trk.quarterLength * n_samples


    def Occupation_Rate(self, trk: stream):

        occ_rate = 0

        t = trk.asTimespans(classList=(note.Note,), flatten=True)

        for offset in [float(n) / 100 for n in range(0, 3225, 25)]:

            o = t.getVerticalityAt(offset)

            if len(o.pitchSet) >= 1:

                occ_rate = occ_rate + 1

            else:
                pass

        return occ_rate / (trk.quarterLength * n_samples)



    def Polyphonic_Rate(self, trk: stream):

        count = 0

        t = trk.asTimespans(classList=(note.Note,), flatten=True)


        for v in t.iterateVerticalities():

            c = v.startTimespans

            if len(c) > 1:

                count = count + 1

            elif len(c) <= 1:
                pass

        return count / self.Number_of_notes(trk)[0]



    def Pitch_Range_Descriptors(self, trk: stream):

        mnotes = []

        partStream = trk.parts.stream()

        for n in partStream.recurse().notes:

            if n.isNote == True:

                mnotes.append(n.pitch.midi)
            
            elif n.isChord == chord.Chord():
                print('CHORD!')
                continue

        max_note = max(mnotes)
        min_note = min(mnotes)
    
        mean = sum(mnotes) / len(mnotes)
        std_dev = np.std(mnotes)

        return max_note / trk.quarterLength * n_samples, min_note / trk.quarterLength * n_samples, mean / trk.quarterLength * n_samples, std_dev / trk.quarterLength * n_samples



    def Pitch_Interval_Range(self, trk: stream):

        intrval = []

        for part in trk.parts:
            c = []

            for n in part.recurse().notes:
                c.append(n)

            for i, n in enumerate(c):

                if i == 0:
                    pass

                else:
                    pre = c[i-1]
                    d = interval.Interval(pre, n)
                    intrval.append(abs(d.semitones))

        inv_max = max(intrval)
        inv_min = min(intrval)

        inv_mean = sum(intrval) / len(intrval)
        inv_std_dev = np.std(intrval)

        return inv_max / trk.quarterLength * n_samples, inv_min / trk.quarterLength * n_samples, inv_mean / trk.quarterLength * n_samples, inv_std_dev / trk.quarterLength * n_samples


    def Note_Duration(self, trk: stream):

        durations = []
        for n in trk.recurse().notes:
            durations.append(n.duration.quarterLength * 4)
 
        dur_max = max(durations)
        dur_min = min(durations)
    
        dur_mean = sum(durations) / len(durations)
        dur_std_dev = np.std(durations)


        return  dur_max, dur_min, dur_mean, dur_std_dev

        

    def Mahalanobis_Distance(f, dataset_eval_midi):

        x = np.array([Evaluate(f).piece_signature_vector])

        mEvalVector = []

        for file in os.listdir(dataset_eval_midi):

            fE = os.path.join(dataset_eval_midi, file)
            
            mEvalVector.append(Evaluate(fE).piece_signature_vector)

        mEvalVector = np.array(mEvalVector)

        m = np.mean(mEvalVector, axis=0)

        xMm = x - m

        mEvalVector = np.transpose(mEvalVector)

        covM = np.cov(mEvalVector, bias = False)

        invCovM = np.linalg.inv(covM)

        #np.set_printoptions(suppress= True)

        tem = np.dot(xMm, invCovM)
        tem2 = np.dot(tem, np.transpose(xMm))

        mD = np.reshape(np.sqrt(tem2), -1)

        return mD