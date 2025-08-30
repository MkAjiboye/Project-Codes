{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "5db83fc3-a4ec-4bb4-9477-07761489b5e0",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Map saved as flood_map_overlay.html – open it in browser and screenshot.\n"
     ]
    }
   ],
   "source": [
    "import folium\n",
    "import pandas as pd\n",
    "\n",
    "map_center = [51.4545, -2.5879]  # Bristol lat/lon\n",
    "\n",
    "# Creating folium map\n",
    "m = folium.Map(location=map_center, zoom_start=9)\n",
    "\n",
    "# Flood-prone zones (from EA records)\n",
    "flood_zones = [\n",
    "    {\"name\": \"Somerset Levels\", \"coords\": [51.1, -2.8]},\n",
    "    {\"name\": \"Avonmouth\", \"coords\": [51.5, -2.7]},\n",
    "    {\"name\": \"Bridgwater\", \"coords\": [51.13, -3.0]}\n",
    "]\n",
    "\n",
    "for zone in flood_zones:\n",
    "    folium.Marker(\n",
    "        location=zone[\"coords\"],\n",
    "        popup=f\"Flood-prone: {zone['name']}\",\n",
    "        icon=folium.Icon(color=\"blue\", icon=\"info-sign\")\n",
    "    ).add_to(m)\n",
    "\n",
    "# Model Predictions (from my CSV logs)\n",
    "predictions = [\n",
    "    {\"location\": \"Prediction A\", \"coords\": [51.2, -2.9]},\n",
    "    {\"location\": \"Prediction B\", \"coords\": [51.45, -2.6]}\n",
    "]\n",
    "\n",
    "for pred in predictions:\n",
    "    folium.Marker(\n",
    "        location=pred[\"coords\"],\n",
    "        popup=f\"Predicted High Risk: {pred['location']}\",\n",
    "        icon=folium.Icon(color=\"red\", icon=\"warning-sign\")\n",
    "    ).add_to(m)\n",
    "\n",
    "# Saving map as HTML (can be opened in browser)\n",
    "m.save(\"flood_map_overlay.html\")\n",
    "print(\"Map saved as flood_map_overlay.html – open it in browser and screenshot.\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
