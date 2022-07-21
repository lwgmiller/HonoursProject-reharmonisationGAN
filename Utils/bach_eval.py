
def Beat_Harmonised_Check(trk: stream):

    i = 0
    harmonised = 0
    notHarmonised = 0

    chords = trk.chordify()

    t = trk.asTimespans(classList=(note.Note,), flatten=True)

    

    for v in t.iterateVerticalities():

        if v.offset.is_integer():

            c = v.startTimespans

            if len(c) > 1:

                harmonised = harmonised + 1
                i = i + 1

            elif len(c) <= 1:

                notHarmonised = notHarmonised + 1
                i = i + 1

            elif len(c) > 4:

                print("Error! Too many notes at beat: %s, for the number of voices: %s" % (v.offset, len(trk.parts)))

    

    print("Beat Harmonisation Check Results: ")
    print()
    print("Number of beats: %s" % (n_samples*beat_resolution*n_measures))
    print("number of beats to be harmonised: %s" %(i))
    print("Number of beats Harmonised: %s" %(harmonised))
    print("Number of beats not harmonised: %s" %(notHarmonised))
    print()

    toBeHarm = i

    return toBeHarm, harmonised, notHarmonised

def Consecutive_intervals(trk: stream):

    sopAlt = stream.Score(id='sopAlt')
    sopTen = stream.Score(id='sopTen')
    sopBass = stream.Score(id='sopBass')
    altTen = stream.Score(id='altTen')
    altBass = stream.Score(id='altBass')
    tenBass = stream.Score(id='tenBass')

    sopAlt.insert(0, trk.parts[0])
    sopAlt.insert(0, trk.parts[1])
    sopTen.insert(0, trk.parts[0])
    sopTen.insert(0, trk.parts[2])
    sopBass.insert(0, trk.parts[0])
    sopBass.insert(0, trk.parts[3])
    altTen.insert(0, trk.parts[1])
    altTen.insert(0, trk.parts[2])
    altBass.insert(0, trk.parts[1])
    altBass.insert(0, trk.parts[3])
    tenBass.insert(0, trk.parts[2])
    tenBass.insert(0, trk.parts[3])

    trackCombos = []

    sA = sopAlt.chordify(addPartIdAsGroup=True)
    sT = sopTen.chordify(addPartIdAsGroup=True)
    sB = sopBass.chordify(addPartIdAsGroup=True)
    aT = altTen.chordify(addPartIdAsGroup=True)
    aB = altBass.chordify(addPartIdAsGroup=True)
    tB = tenBass.chordify(addPartIdAsGroup=True)


    trackCombos.append(sA)
    trackCombos.append(sT)
    trackCombos.append(sB)
    trackCombos.append(aT)
    trackCombos.append(aB)
    trackCombos.append(tB)


    parallelFifths = 0
    parallelOctaves = 0

    inv = interval.Interval('P5')
    inv = inv.simpleNiceName

    print("Consecutive Intervals Check Results: ")
    print()
    
    for i in trackCombos:

        pre = str
        chordPrev = chord.Chord()

        for c in i.recurse().notes:

            #print(c.notes)
            

            if len(c) == 2: 
     
                #print(c)
                #print(chordPrev)
 
                intrval = interval.Interval(c.notes[0], c.notes[1]) #c.annotateIntervals(stripSpecifiers=False, returnList=True) 
                intrval = intrval.semiSimpleNiceName

            
                
                if intrval == 'Perfect Fifth' and pre == 'Perfect Fifth':

                    if c.notes[0].nameWithOctave == chordPrev.notes[0].nameWithOctave and c.notes[1].nameWithOctave == chordPrev.notes[1].nameWithOctave:
                        continue

                    else:

                        print("Consecutive fifth found in measure %s" % (c.measureNumber))

                        parallelFifths = parallelFifths + 1
                        pre = intrval
                        chordPrev = c

                if intrval == 'Perfect Octave' and pre == 'Perfect Octave':

                    if c.notes[0].nameWithOctave == chordPrev.notes[0].nameWithOctave and c.notes[1].nameWithOctave == chordPrev.notes[1].nameWithOctave:
                        
                        continue
                    else:

                        print("Consecutive octave found in measure %s" % (c.measureNumber))
                        parallelOctaves = parallelOctaves + 1
                        pre = intrval
                        chordPrev = c

                else:
                    pre = intrval
                    chordPrev = c
    
            elif len(c) > 2:

                print("ERROR! the number of notes at a timestep should not be greater than the number of voices.") # unit test chord greater than 2. also test fifths and octaves at the start/end of pieces
                continue

            elif len(c) < 2:
                continue
        

            #print(intrval)
    print()
    print("Consecutive fifths: %s" % (parallelFifths))
    print("Consecutive octaves: %s" % (parallelOctaves))
    print()

    return parallelFifths, parallelOctaves

def Voice_Leading(trk: stream): #NEED TO TAKE AVERAGE NUMBER OF INTERVALS FOR ALL BACH PIECES

    z = []
    illegalCount = 0
    trackIntervals = {}
    

    for semitones in range(14):
        tempInt = interval.Interval(semitones)
        z.append(tempInt.niceName)
        #print(semitones, tempInt.niceName)


    for part in trk:

        dict = {}

        intervals = []
        illegalIntervals = ['Diminished Fifth', 'Major Seventh', 'Minor Seventh']

        print()
        print(part.partName)
        print()
        for n in part.flatten().recurse().notes:

            intv = interval.Interval(n, n.next())
            intervals.append(intv.niceName)

            for x in illegalIntervals:
                if intv.niceName == x:

                    print("The %s voice contains a '%s' melodic interval!" % (part.partName, x)) #Unit test for chatchin illegal intervals.
                    print()

                    illegalCount = illegalCount+1

        l = Counter()
        for i in z:
            l[i] = intervals.count(i)
            
        for key, value in l.items():
            print(key, value)

            dict[key] = value
        
        trackIntervals[part.partName] = dict

    return illegalCount, trackIntervals    

def Voice_Ranges(trk: stream):

    s = trk.parts[0]
    a = trk.parts[1]
    t = trk.parts[2]
    b = trk.parts[3]

    sBroken = 0
    aBroken = 0
    tBroken = 0
    bBroken = 0

    for n in s.recurse().notes:

        if n.pitch.midi > 81 or n.pitch.midi < 60:

            print("Pitch %s is out of the standard Soprano voice range!" % (n.nameWithOctave))

            sBroken = sBroken+1

        else:
            continue
    
    for n in a.recurse().notes:

        if n.pitch.midi > 76 or n.pitch.midi < 55:

            print("Pitch %s is out of the standard Alto voice range!" % (n.nameWithOctave))

            aBroken = aBroken+1


        else:
            continue

    for n in t.recurse().notes:


        if n.pitch.midi > 69 or n.pitch.midi < 48:


            print("Pitch %s is out of the standard Tenor voice range!" % (n.nameWithOctave))

            tBroken = tBroken+1


        else:
            continue

    
    for n in b.recurse().notes:

        if n.pitch.midi > 64 or n.pitch.midi < 41:

            print("Pitch %s is out of the standard Bass voice range!" % (n.nameWithOctave))

            bBroken = bBroken+1


        else:
            continue
    
    return sBroken, aBroken, tBroken, bBroken

    


def Chord_Analysis(trk:stream):

    chordList = []

    rnList = []

    chordDict = {}

    rnDict = {}


    f = trk.analyze('key')

    typicalChords = ['major triad', 'minor triad', 'major seventh chord', 'minor seventh chord', 'dominant seventh chord', 'diminished triad']

    majorKeyChordPositions = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'Vii']

    minorKeyChordPositions = ['i', 'ii', 'III', 'iv', 'v', 'VI', 'VII']


    chords = trk.chordify()


    for c in chords.recurse().notes:

        c.closedPosition(forceOctave=4, inPlace=True)


        if c.offset.is_integer():

            chordList.append(c.commonName)
            
            rn = roman.romanNumeralFromChord(c, f)

            rnList.append(rn.romanNumeral)

            #c.addLyric(str(rn.figure))


    
    tC = Counter()

    for i in typicalChords:

        tC[i] = chordList.count(i)

    print("Number of typical chords found in a Bach chorale: ")
    print()
    for key, value in tC.items():

        print(key, value)

        chordDict[key] = value

    print()

    if f.mode == 'major':

        cP = Counter()

        for i in majorKeyChordPositions:

            cP[i] = rnList.count(i)


        print("for the key of %s, the following chord positions were used: " % (f))
        print()
        for key, value in cP.items():

            print(key, value)

            rnDict[key] = value

        print()

    elif f.mode =='minor':

        mCP = Counter()

        for i in minorKeyChordPositions:

            mCP[i] = rnList.count(i)

        
        print("for the key of %s, the following chord positions were used: " % (f))
        print()
        for key, value in mCP.items():

            print(key, value)

            rnDict[key] = value

        print()

    else:
        print("something is wrong! the key of this piece is neither major nor minor!")
    
    #trk.insert(0, chords)

    
    #trk.measures(0, 8).show()

    print(chordDict)
    print(rnDict)

    return chordDict, rnDict


def Cadences(trk: stream):
    
    plagualCount = 0
    perfectCount = 0
    chords = trk.chordify()

    f = trk.analyze('key')

    rnPre = roman.RomanNumeral()

    for c in chords.recurse().notes:

        #c.closedPosition(forceOctave=4, inPlace=True)

        rn = roman.romanNumeralFromChord(c, f)

        #c.addLyric(str(rn.figure))


        if (rn.figure == 'I' and rnPre.figure == 'IV') or (rn.figure == 'i' and rnPre.figure == 'iv'):

            print("Plagual cadence in measure %s" % (c.measureNumber))

            plagualCount = plagualCount+1

            rnPre = rn

        elif (rn.figure == 'I' and rnPre.figure == 'V') or (rn.figure == 'i' and rnPre.figure == 'v'):

            print("Perfect cadence found in measure %s" % (c.measureNumber))

            perfectCount = perfectCount+1
            rnPre = rn
        
        else:
            rnPre = rn
    
    return perfectCount, plagualCount
