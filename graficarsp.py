import tkinter as tk
from tkinter import Canvas, Label, Button

# Global state representing the PDDL problem, including locations, robot (with battery), and sacchetti.
state = {
    "locations": {
        "A": {
            "articles": ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "a10"],
            "sacchetti": []  # No sacchetto in A
        },
        "B": {
            "articles": [],
            "sacchetti": ["s1", "s2"]  # Sacchetti start in B
        },
        "C": {
            "articles": [],
            "sacchetti": []
        }
    },
    "robot": {
        "location": "A",      # Initial robot location
        "holding": None,      # Robot is not holding any object initially
        "battery": 3          # Initial battery level = 3
    },
    "sacchetti": {
        "s1": {"articles": [], "full": False, "location": "B"},
        "s2": {"articles": [], "full": False, "location": "B"}
    }
}

# Plan: a list of action steps to reach the goal.
# In this example, articles a1..a5 go into s1 and a6..a10 go into s2.
plan = [
    ("pick-up", {"article": "a1"}),
    ("move", {"to_loc": "B"}),
    ("drop-onto-sacchetto", {"sacchetto": "s1"}),
    ("move", {"to_loc": "A"}),

    ("pick-up", {"article": "a2"}),
    ("move", {"to_loc": "B"}),
    ("drop-onto-sacchetto", {"sacchetto": "s1"}),
    ("move", {"to_loc": "A"}),

    ("pick-up", {"article": "a3"}),
    ("move", {"to_loc": "B"}),
    ("drop-onto-sacchetto", {"sacchetto": "s1"}),
    ("move", {"to_loc": "A"}),

    ("pick-up", {"article": "a4"}),
    ("move", {"to_loc": "B"}),
    ("drop-onto-sacchetto", {"sacchetto": "s1"}),
    ("move", {"to_loc": "A"}),

    ("pick-up", {"article": "a5"}),
    ("move", {"to_loc": "B"}),
    ("drop-onto-sacchetto", {"sacchetto": "s1"}),
    # When moving sacchetto s1, the robot will also be shifted to C.
    ("move-sacchetto-to-C", {"sacchetto": "s1"}),

    ("move", {"to_loc": "A"}),

    ("pick-up", {"article": "a6"}),
    ("move", {"to_loc": "B"}),
    ("drop-onto-sacchetto", {"sacchetto": "s2"}),
    ("move", {"to_loc": "A"}),

    ("pick-up", {"article": "a7"}),
    ("move", {"to_loc": "B"}),
    ("drop-onto-sacchetto", {"sacchetto": "s2"}),
    ("move", {"to_loc": "A"}),

    ("pick-up", {"article": "a8"}),
    ("move", {"to_loc": "B"}),
    ("drop-onto-sacchetto", {"sacchetto": "s2"}),
    ("move", {"to_loc": "A"}),

    ("pick-up", {"article": "a9"}),
    ("move", {"to_loc": "B"}),
    ("drop-onto-sacchetto", {"sacchetto": "s2"}),
    ("move", {"to_loc": "A"}),

    ("pick-up", {"article": "a10"}),
    ("move", {"to_loc": "B"}),
    ("drop-onto-sacchetto", {"sacchetto": "s2"}),
    # Similarly, moving sacchetto s2 will also move the robot to C.
    ("move-sacchetto-to-C", {"sacchetto": "s2"}),
]

class PlannerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Letseat PDDL Simulation with Battery")
        
        # Canvas for drawing locations, articles, sacchetti, and the robot.
        self.canvas = Canvas(self.master, width=700, height=350, bg="white")
        self.canvas.pack()

        # Status label for current action messages.
        self.status_label = Label(self.master, text="Simulation ready", font=("Arial", 12))
        self.status_label.pack()

        # Button to proceed to the next step.
        self.next_button = Button(self.master, text="Next Step", command=self.run_next_step, font=("Arial", 12))
        self.next_button.pack(pady=5)
        
        # Battery status label (placed under the command controls).
        self.battery_label = Label(self.master, text="Battery: " + str(state["robot"]["battery"]), font=("Arial", 12))
        self.battery_label.pack(pady=5)

        # Coordinates for the three locations: A, B, and C.
        self.locations_coords = {
            "A": (50, 50, 200, 200),
            "B": (250, 50, 400, 200),
            "C": (450, 50, 600, 200)
        }

        self.plan_index = 0
        self.update_canvas()

    def update_canvas(self):
        """Clears and redraws the entire scene based on the current state,
        and updates the battery label."""
        self.canvas.delete("all")
        # Draw each location rectangle with a label.
        for loc, coords in self.locations_coords.items():
            x1, y1, x2, y2 = coords
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="#f0f0f0")
            self.canvas.create_text((x1+x2)//2, y1 - 10, text="Location " + loc, font=("Arial", 12, "bold"))
        
        # Draw articles in each location as small blue ovals with labels.
        for loc, content in state["locations"].items():
            articles = content["articles"]
            rect = self.locations_coords[loc]
            start_x = rect[0] + 10
            start_y = rect[1] + 10
            spacing = 20
            for idx, article in enumerate(articles):
                row = idx // 3
                col = idx % 3
                ax = start_x + col * spacing
                ay = start_y + row * spacing
                self.canvas.create_oval(ax, ay, ax+10, ay+10, fill="blue")
                self.canvas.create_text(ax+5, ay+15, text=article, font=("Arial", 7))
        
        # Draw sacchetti in the appropriate locations.
        for loc, content in state["locations"].items():
            sacchetti = content["sacchetti"]
            rect = self.locations_coords[loc]
            start_x = rect[0] + 10
            start_y = rect[3] - 40  # Position sacchetti near the bottom.
            for idx, sacchetto in enumerate(sacchetti):
                sx = start_x + idx*70
                sy = start_y
                self.canvas.create_rectangle(sx, sy, sx+60, sy+30, outline="darkgreen", fill="lightgreen")
                self.canvas.create_text(sx+30, sy+15, text=sacchetto, font=("Arial", 10, "bold"))
                articles_in_sac = state["sacchetti"][sacchetto]["articles"]
                self.canvas.create_text(sx+30, sy+45, text="[" + ",".join(articles_in_sac) + "]", font=("Arial", 8))
                if state["sacchetti"][sacchetto]["full"]:
                    self.canvas.create_text(sx+30, sy+60, text="FULL", fill="red", font=("Arial", 10, "bold"))
        
        # Draw the robot as a red circle in the center of its current location.
        robot_loc = state["robot"]["location"]
        rect = self.locations_coords[robot_loc]
        rx = (rect[0]+rect[2])//2
        ry = (rect[1]+rect[3])//2
        self.canvas.create_oval(rx-15, ry-15, rx+15, ry+15, fill="red")
        self.canvas.create_text(rx, ry, text="R", fill="white", font=("Arial", 14, "bold"))
        if state["robot"]["holding"]:
            self.canvas.create_text(rx, ry+25, text="Holding: " + state["robot"]["holding"], font=("Arial", 10))
        
        # Update the battery status label.
        self.battery_label.config(text="Battery: " + str(state["robot"]["battery"]))

    def run_next_step(self):
        """Executes the next step in the plan and updates the GUI."""
        if self.plan_index >= len(plan):
            self.status_label.config(text="Plan completed!")
            self.next_button.config(state="disabled")
            return

        step = plan[self.plan_index]
        action, params = step
        msg = f"Step {self.plan_index+1}: {action} {params}"
        self.status_label.config(text=msg)

        # Execute corresponding action.
        if action == "pick-up":
            self.action_pick_up(**params)
        elif action == "move":
            self.action_move(**params)
        elif action == "drop-onto-sacchetto":
            self.action_drop_onto_sacchetto(**params)
        elif action == "move-sacchetto-to-C":
            self.action_move_sacchetto_to_C(**params)
        else:
            self.status_label.config(text=f"Unknown action: {action}")

        self.plan_index += 1
        # Refresh the canvas to reflect updated state.
        self.update_canvas()

    def action_pick_up(self, article):
        """Robot picks up an article, if present in the current location."""
        loc = state["robot"]["location"]
        if state["robot"]["holding"] is not None:
            print("Error: Robot is already holding an object!")
            return
        if article in state["locations"][loc]["articles"]:
            state["locations"][loc]["articles"].remove(article)
            state["robot"]["holding"] = article
        else:
            print(f"Error: Article {article} not found in location {loc}.")

    def action_move(self, to_loc):
        """Robot moves to a different location."""
        if to_loc not in state["locations"]:
            print("Error: Invalid destination!")
            return
        state["robot"]["location"] = to_loc

    def action_drop_onto_sacchetto(self, sacchetto):
        """Robot drops the article it is holding onto a sacchetto in the current location.
           This action decreases the battery by 1 and, if depleted, moves the robot to B for recharge."""
        loc = state["robot"]["location"]
        if state["robot"]["holding"] is None:
            print("Error: Nothing to drop!")
            return
        if sacchetto in state["locations"][loc]["sacchetti"]:
            article = state["robot"]["holding"]
            state["robot"]["holding"] = None
            state["sacchetti"][sacchetto]["articles"].append(article)
            # Decrement battery by 1.
            state["robot"]["battery"] -= 1
            # Mark the sacchetto as full if it reaches 5 articles.
            if len(state["sacchetti"][sacchetto]["articles"]) == 5:
                state["sacchetti"][sacchetto]["full"] = True
            # If the battery is depleted, move the robot to B to recharge.
            if state["robot"]["battery"] == 0:
                self.status_label.config(text="Battery depleted! Moving to B for recharge.")
                if state["robot"]["location"] != "B":
                    state["robot"]["location"] = "B"
                    self.update_canvas()
                self.action_recharge()
        else:
            print(f"Error: Sacchetto {sacchetto} not found in location {loc}.")

    def action_recharge(self):
        """Simulate the recharge action:
           When the robot is in location B and its battery is 0, restore the battery to 3."""
        loc = state["robot"]["location"]
        if loc != "B":
            print("Error: Robot must be in B to recharge!")
            return
        if state["robot"]["battery"] == 0:
            state["robot"]["battery"] = 3
            self.status_label.config(text="Robot recharged at B, battery now at 3.")
        else:
            print("Battery is not depleted; recharge not needed.")

    def action_move_sacchetto_to_C(self, sacchetto):
        """
        Moves the sacchetto from location B to C if it is full and, along with that,
        moves the robot to location C.
        """
        if state["robot"]["location"] != "B":
            print("Error: Robot must be in B to move a sacchetto!")
            return
        if sacchetto in state["locations"]["B"]["sacchetti"]:
            if state["sacchetti"][sacchetto]["full"]:
                state["locations"]["B"]["sacchetti"].remove(sacchetto)
                state["locations"]["C"]["sacchetti"].append(sacchetto)
                state["sacchetti"][sacchetto]["location"] = "C"
                # Additionally move the robot to location C.
                state["robot"]["location"] = "C"
            else:
                print(f"Error: Sacchetto {sacchetto} is not full!")
        else:
            print(f"Error: Sacchetto {sacchetto} not found in location B.")

if __name__ == '__main__':
    root = tk.Tk()
    app = PlannerGUI(root)
    root.mainloop()
