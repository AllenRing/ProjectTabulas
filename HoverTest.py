Drone Hover Function



Front = 0
Back = 0
Left = 0
Right = 0


min = 180
strength = 190

while(true){
pitch = #getpitch
roll = #getroll

range = (strength - min)

Right = ((roll / float(30)) * range)
Left = -1 * ((roll / float(30)) * range)

Front = -1 * ((pitch / float(30)) * range)
Back = ((pitch / float(30)) * range)

#sets the motors actual values
BRM = Back + Right + strength
BLM = Back + Left + strength
FRM = Front + Right = strength
FLM = Front + Left + strength
}# end of while
