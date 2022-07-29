from music21 import *
from collections import Counter




# Function for Beat Harmonisation check
def Beat_Harmonised_Check(trk: stream):

    i = 0
    harmonised = 0
    notHarmonised = 0

    chords = trk.chordify()

    t = trk.asTimespans(classList=(note.Note,), flatten=True)

    
	# Iterates through "verticalities" (timesteps containing all track information)
    for v in t.iterateVerticalities():

        if v.offset.is_integer():

			# Only specifies a pitch in a timestep if the pitch began in that timestep.
            c = v.startTimespans

			#Checks to see if a note has been harmonised or not
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

#Function to calculate consecutive errors
def Consecutive_intervals(trk: stream):

	#Turns music21 track information into streams
    sopAlt = stream.Score(id='sopAlt')
    sopTen = stream.Score(id='sopTen')
    sopBass = stream.Score(id='sopBass')
    altTen = stream.Score(id='altTen')
    altBass = stream.Score(id='altBass')
    tenBass = stream.Score(id='tenBass')

	#splits tracks into variables with one other voice.
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

	#Converts every voice comb to only contain chords
    sA = sopAlt.chordify()
    sT = sopTen.chordify()
    sB = sopBass.chordify()
    aT = altTen.chordify()
    aB = altBass.chordify()
    tB = tenBass.chordify()


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

		#defines the previous chord
        pre = str
        chordPrev = chord.Chord()

        for c in i.recurse().notes:            

            if len(c) == 2: 
 
                intrval = interval.Interval(c.notes[0], c.notes[1])
                intrval = intrval.semiSimpleNiceName

				#Check for consecutive fifth
                if intrval == 'Perfect Fifth' and pre == 'Perfect Fifth':

                    if c.notes[0].nameWithOctave == chordPrev.notes[0].nameWithOctave and c.notes[1].nameWithOctave == chordPrev.notes[1].nameWithOctave:
                        continue

                    else:

                        print("Consecutive fifth found in measure %s" % (c.measureNumber))

                        parallelFifths = parallelFifths + 1
                        pre = intrval
                        chordPrev = c

				#Checks for consecutive octave
                if intrval == 'Perfect Octave' and pre == 'Perfect Octave':

					#Checks to make sure the pitches change while remaining a consecutive 0ctave
                    if c.notes[0].nameWithOctave == chordPrev.notes[0].nameWithOctave and c.notes[1].nameWithOctave == chordPrev.notes[1].nameWithOctave:
                        
                        continue
                    else:

                        print("Consecutive octave found in measure %s" % (c.measureNumber))
                        parallelOctaves = parallelOctaves + 1
                        pre = intrval
                        chordPrev = c

                else:
				#Increments the prvious interval
                    pre = intrval
                    chordPrev = c
    
            elif len(c) > 2:
			
			# error printed if there are more notes in a timestep than voices
                print("ERROR! the number of notes at a timestep should not be greater than the number of voices.") 
                continue

            elif len(c) < 2:
                continue
        

    print()
    print("Consecutive fifths: %s" % (parallelFifths))
    print("Consecutive octaves: %s" % (parallelOctaves))
    print()

    return parallelFifths, parallelOctaves

#Function to conduct voice leading checks.
def Voice_Leading(trk: stream): 

    z = []
    illegalCount = 0
    trackIntervals = {}
    
	#Creates the list of intervals in the voice.
    for semitones in range(14):
        tempInt = interval.Interval(semitones)
        z.append(tempInt.niceName)


    for part in trk:

        dict = {}

        intervals = []
		
		#Defines the illegal intervals to be checked
        illegalIntervals = ['Diminished Fifth', 'Major Seventh', 'Minor Seventh']

        print()
        print(part.partName)
        print()
        for n in part.flatten().recurse().notes:

            intv = interval.Interval(n, n.next())
            intervals.append(intv.niceName)
			
			#Checks for illegal intervals
            for x in illegalIntervals:
                if intv.niceName == x:

                    print("The %s voice contains a '%s' melodic interval!" % (part.partName, x)) #Unit test for chatchin illegal intervals.
                    print()

                    illegalCount = illegalCount+1

        l = Counter()
        for i in z:
            l[i] = intervals.count(i)
			
        #Apps the interval name and count to a dictionary
        for key, value in l.items():
            print(key, value)

            dict[key] = value
        
        trackIntervals[part.partName] = dict

    return illegalCount, trackIntervals    

#Function to discover any voice range errors, as well as the existence of multiple notes in a single voice.
def Voice_Ranges(trk: stream):

    s = trk.parts[0]
    a = trk.parts[1]
    t = trk.parts[2]
    b = trk.parts[3]

    sBroken = 0
    aBroken = 0
    tBroken = 0
    bBroken = 0
    voiceChords = 0

	#Check for soprano voice
    for n in s.recurse().notes:

        if n.isChord == True:

            print("%s voice contains a chord!" % s.partName)
            print()

            voiceChords = voiceChords + 1

            for p in n.notes:
            
                if p.pitch.midi > 81 or p.pitch.midi < 60:

                    print("Pitch %s is out of the standard Soprano voice range!" % (p.nameWithOctave))

                    sBroken = sBroken+1

        elif n.isNote == True:
        
            if n.pitch.midi > 81 or n.pitch.midi < 60:

                print("Pitch %s is out of the standard Soprano voice range!" % (n.nameWithOctave))

                sBroken = sBroken+1
            

        else:
            continue
    #Check for alto voice
    for n in a.recurse().notes:

        if n.isChord == True:

            print("%s voice contains a chord!" % a.partName)
            print()

            voiceChords = voiceChords + 1

            for p in n.notes:
                
                if p.pitch.midi > 76 or p.pitch.midi < 55:

                    print("Pitch %s is out of the standard Alto voice range!" % (p.nameWithOctave))

                    aBroken = aBroken+1

        elif n.isNote == True:
            
            if n.pitch.midi > 76 or n.pitch.midi < 55:

                print("Pitch %s is out of the standard Alto voice range!" % (n.nameWithOctave))

                aBroken = aBroken+1


        else:
            continue
	#Check for tenor voice
    for n in t.recurse().notes:


        if n.isChord == True:

            print("%s voice contains a chord!" % t.partName)
            print()

            voiceChords = voiceChords + 1

            for p in n.notes:
                
                if p.pitch.midi > 69 or p.pitch.midi < 48:

                    print("Pitch %s is out of the standard Tenor voice range!" % (p.nameWithOctave))

                    tBroken = tBroken+1

        elif n.isNote == True:
            
            if n.pitch.midi > 69 or n.pitch.midi < 48:

                print("Pitch %s is out of the standard Tenor voice range!" % (n.nameWithOctave))

                tBroken = tBroken+1


        else:
            continue

	#Check for bass voice
    for n in b.recurse().notes:

        if n.isChord == True:

            print("%s voice contains a chord!" % b.partName)
            print()

            voiceChords = voiceChords + 1

            for p in n.notes:
                
                if p.pitch.midi > 64 or p.pitch.midi < 41:

                    print("Pitch %s is out of the standard Tenor voice range!" % (p.nameWithOctave))

                    bBroken = bBroken+1

        elif n.isNote == True:
            
            if n.pitch.midi > 64 or n.pitch.midi < 41:

                print("Pitch %s is out of the standard Tenor voice range!" % (n.nameWithOctave))

                bBroken = bBroken+1


        else:
            continue
    
    return sBroken, aBroken, tBroken, bBroken, voiceChords

    

#Function to perform the chord analysis
def Chord_Analysis(trk:stream):

    chordList = []

    rnList = []

    chordDict = {}

    rnDict = {}


    f = trk.analyze('key')

	#Defining the typical chords found in a chorale.
    typicalChords = ['major triad', 'minor triad', 'major seventh chord', 'minor seventh chord', 'dominant seventh chord', 'diminished triad']

	#Defining the major chord positions
    majorKeyChordPositions = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'Vii']

	#Defining the minor chord positions
    minorKeyChordPositions = ['i', 'ii', 'III', 'iv', 'v', 'VI', 'VII']

	#Tracks are turned into chords
    chords = trk.chordify()


    for c in chords.recurse().notes:

        c.closedPosition(forceOctave=4, inPlace=True)


        if c.offset.is_integer():

            chordList.append(c.commonName)
            
            rn = roman.romanNumeralFromChord(c, f)

            rnList.append(rn.romanNumeral)

    
    tC = Counter()

    for i in typicalChords:

        tC[i] = chordList.count(i)

    print("Number of typical chords found in a Bach chorale: ")
    print()
    for key, value in tC.items():

        print(key, value)

        chordDict[key] = value

    print()

	#if the key is major, use major chord positions
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

	#If the key is minor, use the minor chord positions
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
    


    print(chordDict)
	print()
    print(rnDict)

    return chordDict, rnDict

#Function to perform cadence check
def Cadences(trk: stream):
    
    plagalCount = 0
    perfectCount = 0
    chords = trk.chordify()

	#Find the key of the piece
    f = trk.analyze('key')

    rnPre = roman.RomanNumeral()

    for c in chords.recurse().notes:

        rn = roman.romanNumeralFromChord(c, f)

		#Check for plagal cadences
        if (rn.figure == 'I' and rnPre.figure == 'IV') or (rn.figure == 'i' and rnPre.figure == 'iv'):

            print("Plagal cadence in measure %s" % (c.measureNumber))

            plagalCount = plagalCount+1

            rnPre = rn

		#Check for perfect cadences
        elif (rn.figure == 'I' and rnPre.figure == 'V') or (rn.figure == 'i' and rnPre.figure == 'v'):

            print("Perfect cadence found in measure %s" % (c.measureNumber))

            perfectCount = perfectCount+1
            rnPre = rn
        
        else:
            rnPre = rn
    
    return perfectCount, plagalCount
