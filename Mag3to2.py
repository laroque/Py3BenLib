#!/usr/bin/python3
'''
  A package to convert magfield3 style inputs to those for magfield2. If called from the shell as:
  python3 Mag3to2.py </path/to/input/> </path/to/output>
  Then the conversion is done, creating a new file. The package will also be importable so that it can be used in some larger context or so that pieces can be used.
'''
import os, sys, math

class Mag3to2:
    '''
      Converter from magfield3 input to magfield2 input
    '''

    def __init__(self,mf3file=False,mf2file=False):
        '''
          If input and output files are given then does a "default" magfield3 to magfield2 conversion.

          mf3file: (optional) the filename or path to the magfield3 input file

          mf2file: (optional) the file to create with the magfield2 output
        '''
        if (mf3file and mf2file):
            self.ReadInputFile(mf3file)
            self.EnsureColinear()
            self.ConvertArray()
            self.WriteOutput(mf2file)

    def ReadInputFile(self,filename):
        '''
          Grab the input magfield3 data from a file on disk and store as an attribute
    
          No explicit return values.
        '''
        filecontent = open(filename,'r').readlines()[1:]
        setattr(self,'mf3array',[list(map(float,line.split())) for line in filecontent])

    def EnsureColinear(self):
        '''
          Ensure that all of the magfield3 input coils are colinear.
    
          Returns True if colinear, False otherwise.
        '''
        colinear = True
        #get a vector for the first coil.
        coil0vec = [B-A for A,B in zip(self.mf3array[0][1:4],self.mf3array[0][4:7])]
        #normalize to get a unit vector.
        norm = 0
        for val in coil0vec: norm = norm + val**2
        norm=math.sqrt(norm)
        coil0dir = [val/norm for val in coil0vec]
        for coil in self.mf3array:
            vecA = [B-A for A,B in zip(coil[1:4],self.mf3array[0][1:4])]
            vecB = [B-A for A,B in zip(coil[4:7],self.mf3array[0][1:4])]
            normA = 0
            normB = 0
            for val in vecA: normA = normA + val**2
            for val in vecB: normB = normB + val**2
            normA = math.sqrt(normA)
            normB = math.sqrt(normB)
            if normA !=0:
                dirAfwd = [val/normA for val in vecA]
                dirAbwd = [-val/normA for val in vecA]
            else:
                dirAfwd = coil0dir
                dirAbwd = coil0dir
            if normB !=0:
                dirBfwd = [val/normB for val in vecB]
                dirBbwd = [-val/normB for val in vecB]
            else:
                dirBfwd = coil0dir
                dirBbwd = coil0dir
            colinear = colinear and ((coil0dir == dirAfwd) or (coil0dir == dirAbwd))
            colinear = colinear and ((coil0dir == dirBfwd) or (coil0dir == dirBbwd))
        return colinear

    def ConvertArray(self):
        '''
          Take a list of lists, each of which is a magfield3 coil and produce a corresponding list of lists, each of which is a magfield2 coil.

          The magfield3 data is in self.mf3array

          The produced magfield2 data gets stored as self.mf2array
        '''
        mf2array = []
        for coil in self.mf3array:
            zmid = math.sqrt(((coil[4] + coil[1]) / 2)**2 + ((coil[5] + coil[2])/2)**2 + ((coil[6] + coil[3])/2)**2)
            if (((coil[4] + coil[1]) < 0) or ((coil[5] + coil[2]) < 0) or ((coil[6] + coil[3]) < 0)):
                zmid=-zmid
            rin = coil[7]
            thick = coil[8] - coil[7]
            length = math.sqrt((coil[4]-coil[1])**2+(coil[5]-coil[2])**2+(coil[6]-coil[3])**2)
            cur = coil[0]*(thick)*(length)
            mf2array.append([zmid, rin, thick, length, cur])
        setattr(self,'mf2array',mf2array)

    def WriteOutput(self,filename):
        '''
          Write the computed magfield2 coils to a file in the magfield2 input format.

          The magfield2 coil data comes from self.mf2array


          The output is written to filename.
        '''
        outputfile = open(filename, 'w')
        outputfile.write(str(len(self.mf2array))+'\n')
        for coil in self.mf2array:
            outputfile.write('%f  %f  %f  %f  %f' % tuple(coil) + '\n')
        outputfile.close()

# If called from the terminal, fully convert input file and create an output:
if __name__=='__main__':
    try:
        if len(sys.argv) != 3:
            raise IndexError('The number of inputs is not correct')
        if not os.path.exists(sys.argv[1]):
            raise NameError('file named %s does not exist' % sys.argv[1])
        if os.path.exists(sys.argv[2]):
            raise NameError('file named %s already exists' % sys.argv[2])
        MagConv = Mag3to2(sys.argv[1],sys.argv[2])

    except IndexError:
        print('There is a problem with the inputs provided')
