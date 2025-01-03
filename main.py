import sys
from CONSTANTS import *


class COST:
    # Calculate the total material cost
    @ staticmethod
    def material_cost(weight: float, cost_of_spool):
        return weight * cost_of_spool * MATERIAL_CONSTANT

    # Calculate the total labour cost
    @staticmethod
    def labour_charges(time):
        return PRINT_ASSEMBLY_COST * time

    # Calculate the total printer degradation cost
    @staticmethod
    def running_cost(printing_time):
        return printing_time * PRINTER_RUNNING_COST

    # Calculate the total electricity cost
    @staticmethod
    def electricity_cost(printing_time):
        return printing_time * ELECTRICITY_CHARGES


def time_validation(time):
    time_hours = int(time)
    if time_hours !=0:
        time_minutes = (round(time % time_hours, 2))
    else:
        time_minutes = time
    time_minutes = time_minutes *100
    while time_minutes > 60:
        time = int(
            input("Minutes can't be more than 60. Enter the time in given format(HH.mm):\n"))
        time_minutes = (round(time % time_hours, 2)) * 100

    time_minutes = time_minutes / 60

    return time_hours + time_minutes


def main():
    margin = False
    if len(sys.argv) > 1:
        margin = True
    cost = COST()
    # Start the App
    print("Welcome to 3D printing cost calculator:\n")

    # Get weight of material used to print
    weight_of_material = float(input("Enter the weight of material required to print(Kgs.gm) :\n"))

    # Get the total time for printing
    time_to_print = float(input("Enter the time required to print(HH.mm):\n"))

    assembly_time = input("Enter the time required to Assemble the Print(HH.mm) Enter to skip:\n")
    if assembly_time != '':
        total_assembly_time = time_validation(float(assembly_time))

    else:
        total_assembly_time = 0

    total_printing_time = time_validation(time_to_print)

    total_cost = cost.material_cost(weight_of_material, 1000) + cost.labour_charges(
        total_assembly_time) + cost.running_cost(total_printing_time) + cost.electricity_cost(total_printing_time)

    if margin:
        total_cost = total_cost * MARGIN

    print(f"Total Printing cost {int(total_cost)}")
    print("All well if it ends well")


if __name__ == "__main__":
    main()
