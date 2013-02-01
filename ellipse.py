import pylab as pl
from pylab import det
from numpy import *

class ellipse:
	def __init__(self,SIG):
		self.Sigma = SIG
		self.SigX = self.Sigma[0:2,0:2];
		self.SigY = self.Sigma[2:4,2:4];
		self.SigZ = self.Sigma[4:6,4:6];

		# self.EpsilonX = self.Sigma[0,0]*self.Sigma[1,1] - self.Sigma[0,1]**2
		self.EmittenceX = sqrt(math.fabs(det(self.SigX)))
		self.EmittenceY = sqrt(math.fabs(det(self.SigY)))
		self.EmittenceZ = sqrt(math.fabs(det(self.SigZ)))

		self.TwissXX1 = array([-(self.SigX[0,1]),self.SigX[0,0],self.SigX[1,1],self.EmittenceX**2]/self.EmittenceX)
		self.TwissYY1 = array([-(self.SigY[0,1]),self.SigY[0,0],self.SigY[1,1],self.EmittenceY**2]/self.EmittenceY)
		self.TwissZZ1 = array([-(self.SigZ[0,1]),self.SigZ[0,0],self.SigZ[1,1],self.EmittenceZ**2]/self.EmittenceZ)

		self.WidthX = sqrt(self.TwissXX1[1]*self.TwissXX1[3])
		self.WidthY = sqrt(self.TwissYY1[1]*self.TwissYY1[3])
		self.WidthZ = sqrt(self.TwissZZ1[1]*self.TwissZZ1[3])

		self.EmittenceXY = sqrt( det(matrix([[SIG[0,0],SIG[0,2]] ,[SIG[2,0],SIG[2,2]] ])) )
		self.TwissXY = array([-SIG[0,2],SIG[0,0],SIG[2,2],self.EmittenceXY**2])/self.EmittenceXY

		self.EmittenceXZ = sqrt( det(matrix([[SIG[0,0],SIG[0,4]] ,[SIG[4,0],SIG[4,4]] ])) )
		self.TwissXZ = array([-SIG[0,4],SIG[0,0],SIG[4,4],self.EmittenceXZ**2])/self.EmittenceXZ

		self.EmittenceYZ = sqrt( det(matrix([[SIG[2,2],SIG[2,4]] ,[SIG[4,2],SIG[4,4]] ])) )
		self.TwissYZ = array([-SIG[2,4],SIG[2,2],SIG[4,4],self.EmittenceYZ**2])/self.EmittenceYZ


	def GenerateXY(self,TWISS,NPoints=1000):
		Theta = linspace(0,2*pi,NPoints);
		XPoints = zeros((NPoints),float); YPoints = zeros((NPoints),float)
		m11=math.sqrt(math.fabs(TWISS[1]));
		m21=-TWISS[0]/math.sqrt(math.fabs(TWISS[1]));
		m22=1/math.sqrt(math.fabs(TWISS[1]));
		Radius=math.sqrt(math.fabs(TWISS[3]));
		m12=0;
		PHI = arctan(2.0*TWISS[0]/(TWISS[2]-TWISS[1]))/2.0
		for i in range(NPoints):
			XPoints[i] = Radius*(m11*cos(Theta[i]) + m12*sin(Theta[i]))
			YPoints[i] = Radius*(m21*cos(Theta[i]) + m22*sin(Theta[i]))
		return XPoints,YPoints

	def Plot(self,FIG=0,NPoints=1000,Mod='-',Title = ' '):

		f=pl.figure(FIG)
		f.text(.5, .95, Title, horizontalalignment='center')

		X,Y = self.GenerateXY(self.TwissXX1,NPoints)
		pl.subplot(2,3,1); pl.plot(X,Y,Mod); pl.xlabel('X [mm]');  pl.ylabel('dx/ds [mrad]');

		X,Y = self.GenerateXY(self.TwissYY1,NPoints)
		pl.subplot(2,3,2); pl.plot(X,Y,Mod); pl.xlabel('Y [mm]');  pl.ylabel('dY/ds [mrad]');

		X,Y = self.GenerateXY(self.TwissZZ1,NPoints)
		pl.subplot(2,3,3); pl.plot(X,Y,Mod); pl.xlabel('Z [mm]');  pl.ylabel('dP/P [mrad]');

#		pl.figure(FIG+1)
		X,Y = self.GenerateXY(self.TwissXY,NPoints)
		pl.subplot(2,3,4); pl.plot(X,Y,Mod); pl.xlabel('X [mm]');  pl.ylabel('Y [mm]');
		L = 20; pl.xlim(-L,L); pl.ylim(-L,L)

		X,Y = self.GenerateXY(self.TwissXZ,NPoints)
		pl.subplot(2,3,5); pl.plot(X,Y,Mod); pl.xlabel('X [mm]');  pl.ylabel('Z [mm]');
		L = 20; pl.xlim(-L,L); pl.ylim(-L,L)

		X,Y = self.GenerateXY(self.TwissYZ,NPoints)
		pl.subplot(2,3,6); pl.plot(X,Y,Mod); pl.xlabel('Y [mm]');  pl.ylabel('Z [mm]');
		L = 20; pl.xlim(-L,L); pl.ylim(-L,L)
		
		pl.subplots_adjust( hspace=0.35 )
		pl.subplots_adjust( wspace=0.35 )


#		pl.xlim([-2,2]); pl.ylim([-2,2])










