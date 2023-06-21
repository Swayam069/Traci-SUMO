import os
import sys
import time
from sumolib import checkBinary

# Checks for the SUMO_HOME in the path else print exit.
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

#     import the traci from the file of simulaiton 
import traci
import traci.constants

sumo_binary = checkBinary('sumo-gui')
sumoCmd = [sumo_binary, "-c",
           "path/to/your/SUMO/osm.sumocfg", "--start"]
traci.start(sumoCmd)
print("Starting SUMO")
traci.gui.setSchema("View #0", "real world")

j = 0
 # simulation endtime of the simulation
simulation_endtime = 1500 
output_file = "output.txt"  # Output file name

# Redirect output to a file
original_stdout = sys.stdout
sys.stdout = open(output_file, "w")

while j < simulation_endtime:
  # to increase the speed of simulation
    time.sleep(0.05)  
    traci.simulationStep()
    vehicles = traci.vehicle.getIDList()
# the seconds for which the Code pings for the data
    if j % 1 == 0: 
        for i in range(len(vehicles)):
            vehicle_id = vehicles[i]
            traci.vehicle.setSpeedMode(vehicle_id, 0)
            traci.vehicle.setSpeed(vehicle_id, 0.5)

            speed = traci.vehicle.getSpeed(vehicle_id)
            print("Speed", vehicle_id, ":", speed, "m/s")

            edge_id = traci.vehicle.getRoadID(vehicle_id)
            print("EdgeID of", vehicle_id, ":", edge_id)

            angle = traci.vehicle.getAngle(vehicle_id)
            flangle = "{:.2f}".format(angle)
            print("Angle of", vehicle_id, ":", flangle, "degree")

            position = traci.vehicle.getPosition(vehicle_id)
            x_coord, y_coord = position
            print("Coordinates of", vehicle_id,
                  "are (x:", x_coord, "y:", y_coord, ")")

            simulation_time = traci.simulation.getTime()
            print("Current Simulation Time for",
                  vehicle_id, "is:", simulation_time)

            depart_delay = traci.vehicle.getDepartDelay(vehicle_id)
            print("Depart delay of", vehicle_id, ":", depart_delay, "seconds")

            cocons = traci.vehicle.getCO2Emission(vehicle_id)
            fcocons = "{:.2f}".format(cocons)
            print("Electricity consumption for",
                  vehicle_id, ":", fcocons, "co2")

    j += 1

# Restore output to console
sys.stdout.close()
sys.stdout = original_stdout

# To get network parameters of the vehicle
IDsOfEdges = traci.edge.getIDList()
print("IDs of the edges:", IDsOfEdges)

IDsOfJunctions = traci.junction.getIDList()
print("IDs of junctions:", IDsOfJunctions)

# Always close traci at the end
traci.close()
