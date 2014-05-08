ShooterPlatform
===============

This is a repository on a first-person shooting game for the class "Software Design", Spring 2014, final project at Olin College of Engineering.

Team Members:

Filippos Lymperopoulos
Sidd Singal
James Jang

====================================================================================

The plot:

You are under attack by the military, and you must shoot them to defend
youself. The enemies maneuver around walls and try to shoot back at you. 
Survive as long as you can. This game uses a physical replica gun to shoot
with in the game using openCV libraries. The replica gun is composed of a simple RG LED
along with some resistors connect to a 4-pin button. The gun has a blue marker on it that
serves as the color tracked for the motion of the target, while the ON/OFF stage of the 
LED signals the shooting.

====================================================================================

The program:

This final project consists of an integration between python OOP and OpenCV libraries. The player
has a given health indicated by a health bar. That health decreases as enemies shoot at you, or reach the
end of the display window. An interesting algorithm was implemented that allows the GIFs enemies to scale
and become larger as they approach you. Enemies can hide behind walls and protect themselves, while your
goal is to stay alive! 

====================================================================================

Acknowledgements:

We would like to thank Paul Ruvolo for his guidance and help throughout the project, as well as the
NINJAS, teaching assistants, of the class. A further description of the design of the project is given at the 
following website: https://sites.google.com/site/shooterplatform/design

