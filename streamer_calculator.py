# Model Rocket Streamer Calculator by David Presker

import math
import sys

# Custom Tee class to print and write to file
class Tee:
    def __init__(self, filename, mode="w"):
        self.file = open(filename, mode, encoding="utf-8")
        self.stdout = sys.stdout

    def write(self, message):
        self.stdout.write(message)
        self.file.write(message)

    def flush(self):
        self.stdout.flush()
        self.file.flush()

    def close(self):
        self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def compute_streamer_area(mass_grams, velocity, Cd, air_density, gravity):
    mass = mass_grams / 1000  # grams to kg
    area_m2 = (2 * mass * gravity) / (air_density * Cd * velocity**2)
    area_cm2 = area_m2 * 10000
    return area_m2, area_cm2


def model_rocket_streamer_calculator():
    print("=== Model Rocket Streamer Size Calculator ===")
    print("===            by David Presker            ===\n")

    try:
        project_name = input("Project name (optional): ").strip()

        mass_input = input("Rocket mass (grams) [Required]: ").strip()
        if not mass_input:
            print("❌ Error: Rocket mass is required.")
            return
        mass = float(mass_input)

        velocity_input = input("Descent rate v (m/s) [Default: 6.0]: ").strip()
        velocity = float(velocity_input) if velocity_input else 6.0

        air_density_input = input("Air density ρ (kg/m³) [Default: 1.225]: ").strip()
        air_density = float(air_density_input) if air_density_input else 1.225

        Cd_input = input("Drag coefficient Cd (for streamers: 0.3<Cd<0.8) [Default: 0.4]: ").strip()
        Cd = float(Cd_input) if Cd_input else 0.4

        gravity_input = input("Gravity g (m/s²) [Default: 9.8067]: ").strip()
        gravity = float(gravity_input) if gravity_input else 9.8067

        # Compute required drag area
        area_m2, area_cm2 = compute_streamer_area(mass, velocity, Cd, air_density, gravity)

        # Ask for width
        width_input = input("Streamer width in cm (if width isn't provided, it is going to be auto calculated)(optional): ").strip()
        if width_input:
            width_cm = float(width_input)
            length_cm = area_cm2 / width_cm  # compute required length
            ratio_used = length_cm / width_cm
            width_source = "manual"
        else:
            # Ask for ratio only if width is not set
            ratio_input = input("Length-to-width ratio (ratios between 5:1 and 10:1 are very effective) [Default: 10]: ").strip()
            ratio = float(ratio_input) if ratio_input else 10.0
            width_cm = math.sqrt(area_cm2 / ratio)
            length_cm = width_cm * ratio
            ratio_used = ratio
            width_source = "auto"

        # --- Output ---
        with Tee("streamer.txt") as tee:
            print("=== ✅ Results of Streamer Calculation, by David Presker ===\n", file=tee)
            if project_name:
                print(f"Project name: {project_name}", file=tee)

            print(f"Required drag area: {area_cm2:.2f} cm²", file=tee)
            print(f"Suggested streamer dimensions:", file=tee)
            print(f" - Width:  {width_cm:.1f} cm {'(user input)' if width_source == 'manual' else '(auto-calculated)'}", file=tee)
            print(f" - Length: {length_cm:.1f} cm", file=tee)
            print(f" - Aspect ratio: {ratio_used:.1f} : 1", file=tee)

            print("\n--- Inputs ---", file=tee)
            print(f"Rocket mass: {mass:.1f} g", file=tee)
            print(f"Descent rate: {velocity} m/s", file=tee)
            print(f"Air density: {air_density} kg/m³", file=tee)
            print(f"Drag coefficient: {Cd}", file=tee)
            print(f"Gravity: {gravity} m/s²", file=tee)
            if width_source == "manual":
                print("⚠️  Ratio was calculated because width was manually provided", file=tee)
            else:
                print(f"Used ratio: {ratio:.1f} : 1", file=tee)

            tee.flush()

        print("✅ Results also saved to 'streamer.txt'")

    except ValueError:
        print("❌ Invalid input. Please enter valid numbers.")


# Run the calculator
model_rocket_streamer_calculator()
