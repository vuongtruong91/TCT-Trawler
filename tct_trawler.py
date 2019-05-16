import ROOT as R
import os
import linecache
from array import array

ann = array('i',[ 0 ])
laser = bytearray(21)
temp = array('i',[ 0 ])
diode = bytearray(21)
pair = array('i',[ 0 ])
pairdut = array('f',101*[ 0 ])
biasdut = array('f',101*[ 0. ])
pairref = array('f',2*[ 0 ])
biasref = array('f',2*[ 0. ])


def ReadFile (pairDataFile, pairDataFolder):

  pairDataFiles = pairDataFolder + "/" + pairDataFile
  #print pairDataFiles
  vREF = array('f',2*[ 0. ])   #reference measurements are taken before and after each DUT TCT run   
  vDUT = array('f',101*[ 0. ])
  pairREF = array('f',2*[ 0. ])
  pairDUT = array('f',101*[ 0. ])

  if "results.t" in pairDataFile:
        with open(pairDataFiles, "r") as dut:
          #print pairDataFiles
          txtLines = [line for line in dut]
          #print "First line:", txtLines[0]
          idx = [i for i, line in enumerate(txtLines) if "Voltage(V)" in line][0]
          headers = txtLines[idx].split('\t')
          data = txtLines[idx+1:]
          i = 0
          for line in data:
              words = line.split()
              #print words
              if i < 101:
                 vDUT[i] = float(words[0])
                 pairDUT[i] = float(words[2])
              i += 1
          #print pairDUT
        
  if "results_Ref.t" in pairDataFile:
        with open(pairDataFiles, "r") as ref:
          txtLines = [line for line in ref]
          idx = [i for i, line in enumerate(txtLines) if "Voltage(V)" in line][0]
          headers = txtLines[idx].split('\t')
          data = txtLines[idx+1:]
          j = 0
          for line in data:
              words = line.split()
              if j < 2:
                 vREF[j] = float(words[0])
                 pairREF[j] = float(words[2])
              j += 1
          #print pairREF
        
  return vREF, pairREF, vDUT, pairDUT
    

RTree = R.TTree('pair','PAIR')
RTree.Branch('pair',pair,'pair/I')
RTree.Branch('ann',ann,'ann/I')
RTree.Branch('temp',temp,'temp/I')
RTree.Branch('laser',laser,'laser[21]/C')
RTree.Branch('diode',diode,'diode[21]/C')
RTree.Branch('biasref',biasref,'biasref[118]/F')
RTree.Branch('biasdut',biasdut,'biasdut[118]/F')
RTree.Branch('pairdut',pairdut,'pairdut[118]/F')
RTree.Branch('pairref',pairref,'pairref[118]/F')

def list_files(dir):
   files = []
   for obj in os.listdir(dir):
      if os.path.isfile(os.path.join(dir,obj)):
         files.append(obj)
   return files

def list_dir(dir):
   dirs = []
   for obj in os.listdir(dir):
      if os.path.isdir(os.path.join(dir,obj)):
         dirs.append(obj)
   return dirs

badfiles =[]

for anns in list_dir("."):
   anndir = os.path.join(".",anns)
   ann[0] = int(anns[3])
   for lasers in list_dir(anndir):
      laserdir = os.path.join(anndir,lasers)
      if "redLaserFront" in lasers: pair[0] = 0
      if "redLaserBack" in lasers: pair[0] = 1
      if "irLaser" in lasers: pair[0] = 2
      for i in xrange(len(lasers)):
        if i<21:  laser[i] = lasers[i]
      for temps in list_dir(laserdir):
        tempdir = os.path.join(laserdir, temps)
        temp[0] = int(temps[4:])
        for diodes in list_dir(tempdir):
            diodedir = os.path.join(tempdir,diodes)
            for j in xrange(len(diodes)):
              if j<21:  diode[j] = diodes[j]
            for files in list_files(diodedir):
                   if "results.t" in files:
                     vREF, pairREF, vDUT, pairDUT= ReadFile(files, diodedir)
                     for j in xrange(101):
                       biasdut[j] = vDUT[j]
                       pairdut[j] = pairDUT[j]

                   if "results_Ref.t" in files:
                     vREF, pairREF, vDUT, pairDUT= ReadFile(files, diodedir)
                     for j in xrange(2):
                       biasref[j] = vREF[j]
                       pairref[j] = pairREF[j]
            RTree.Fill()
            #print pairref
print "DONE"


RFile = R.TFile("PAIRS.root",'RECREATE')
RTree.Write("",R.TObject.kOverwrite)
RFile.Close()

