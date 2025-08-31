import math
import sys
import re

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


def compute_streamer_area(mass_kg, velocity, Cd, air_density, gravity):
    """
    mass_kg: kg
    velocity: m/s
    air_density: kg/m³
    gravity: m/s²
    returns area in m²
    """
    area_m2 = (2 * mass_kg * gravity) / (air_density * Cd * velocity**2)
    return area_m2


def model_rocket_streamer_calculator():
    print("===            Model Rocket Streamer Size Calculator             ===")
    print("===                       by David Presker                       ===")
    print("=== https://github.com/kledolin/model_rocket_streamer_calculator ===\n")

    try:
        # --- Unit system selection ---
        unit_system = input("Select unit system: metric (m) [default] or imperial (i): ").strip().lower()
        if unit_system not in ["i", "imperial"]:
            unit_system = "m"

        project_name = input("Project name (optional): ").strip()

        # --- Input prompts ---
        if unit_system == "m":
            mass_unit = "grams"
            velocity_unit = "m/s"
            area_unit = "cm²"
            width_unit = "cm"
            length_unit = "cm"
            default_velocity = 6.0
            default_air_density = 1.225
            default_gravity = 9.8067

            mass_input = float(input(f"Rocket mass ({mass_unit}) [Required]: ").strip())
            mass_kg = mass_input / 1000  # g → kg

            velocity_input = input(f"Descent rate v ({velocity_unit}) [Default: {default_velocity}]: ").strip()
            velocity = float(velocity_input) if velocity_input else default_velocity

            air_density_input = input(f"Air density ρ (kg/m³) [Default: {default_air_density}]: ").strip()
            air_density = float(air_density_input) if air_density_input else default_air_density

            Cd_input = input("Drag coefficient Cd (for streamers: 0.3<Cd<0.8) [Default: 0.4]: ").strip()
            Cd = float(Cd_input) if Cd_input else 0.4

            gravity_input = input(f"Gravity g (m/s²) [Default: {default_gravity}]: ").strip()
            gravity = float(gravity_input) if gravity_input else default_gravity

        else:
            mass_unit = "oz"
            velocity_unit = "ft/s"
            area_unit = "in²"
            width_unit = "in"
            length_unit = "in"
            default_velocity = 20.0  # ft/s
            default_air_density = 1.225  # will be converted to slugs/ft³ for output
            default_gravity = 32.174  # ft/s²

            mass_input = float(input(f"Rocket mass ({mass_unit}) [Required]: ").strip())
            mass_kg = mass_input * 0.0283495  # oz → kg

            velocity_input = input(f"Descent rate v ({velocity_unit}) [Default: {default_velocity}]: ").strip()
            velocity = (float(velocity_input) if velocity_input else default_velocity) * 0.3048  # ft/s → m/s

            air_density_input = input(f"Air density ρ (kg/m³) [Default: {default_air_density}]: ").strip()
            air_density = float(air_density_input) if air_density_input else default_air_density

            Cd_input = input("Drag coefficient Cd (for streamers: 0.3<Cd<0.8) [Default: 0.4]: ").strip()
            Cd = float(Cd_input) if Cd_input else 0.4

            gravity_input = input(f"Gravity g (ft/s²) [Default: {default_gravity}]: ").strip()
            gravity = 9.8067  # metric internally

        # --- Compute area ---
        area_m2 = compute_streamer_area(mass_kg, velocity, Cd, air_density, 9.8067)

        # Convert area to display units
        if unit_system == "m":
            area_display = area_m2 * 10000  # m² → cm²
        else:
            area_display = area_m2 * 1550.0  # m² → in²

        # --- Streamer dimensions ---
        width_input = input(f"Streamer width in {width_unit} (optional): ").strip()
        if width_input:
            width = float(width_input)
            length = area_display / width
            ratio_used = length / width
            width_source = "manual"
        else:
            ratio_input = input("Length-to-width ratio (recommended 5:1 to 10:1) [Default: 10]: ").strip()
            ratio = float(ratio_input) if ratio_input else 10.0
            width = math.sqrt(area_display / ratio)
            length = width * ratio
            ratio_used = ratio
            width_source = "auto"

        # --- Output ---
        fname_safe = re.sub(r'[^\w\d-]', '_', project_name.strip()) if project_name.strip() else "streamer"
        txt_filename = f"streamer_{fname_safe}.txt"

        with Tee(txt_filename) as tee:
            print("===              ✅ Results of Streamer Calculation              ===", file=tee)
            print("===                       by David Presker                       ===", file=tee)
            print("=== https://github.com/kledolin/model_rocket_streamer_calculator ===\n", file=tee)
            if project_name:
                print(f"Project name: {project_name}", file=tee)

            print(f"Required drag area: {area_display:.2f} {area_unit}", file=tee)
            print(f"Suggested streamer dimensions:", file=tee)
            print(f" - Width:  {width:.1f} {width_unit} {'(user input)' if width_source=='manual' else '(auto-calculated)'}", file=tee)
            print(f" - Length: {length:.1f} {length_unit}", file=tee)
            print(f" - Aspect ratio: {ratio_used:.1f}:1", file=tee)

            print("\n--- Inputs ---", file=tee)
            if unit_system == "m":
                print(f"Rocket mass: {mass_input:.1f} g", file=tee)
                print(f"Descent rate: {velocity:.1f} m/s", file=tee)
                print(f"Air density: {air_density:.3f} kg/m³", file=tee)
                print(f"Gravity: 9.81 m/s²", file=tee)
            else:
                print(f"Rocket mass: {mass_input:.1f} oz", file=tee)
                print(f"Descent rate: {(velocity/0.3048):.1f} ft/s", file=tee)
                air_density_imperial = air_density * 0.00194032  # kg/m³ → slugs/ft³
                print(f"Air density: {air_density_imperial:.5f} slugs/ft³", file=tee)
                print(f"Gravity: 32.17 ft/s²", file=tee)

            print(f"Drag coefficient: {Cd}", file=tee)
            if width_source == "manual":
                print("⚠️  Ratio was calculated because width was manually provided", file=tee)
            else:
                print(f"Used ratio: {ratio:.1f}:1", file=tee)

            tee.flush()

        print(f"✅ Results also saved to '{txt_filename}'")

    except ValueError:
        print("❌ Invalid input. Please enter valid numbers.")


# Run the calculator
model_rocket_streamer_calculator()
