import arcpy
import pandas as pd
import matplotlib.pyplot as plt

CrimeDT = r"C:\Users\g2panesa\OneDrive - University of Waterloo\Documents\ArcGIS\Projects\Waterloo Crime Occurence Analysis\Waterloo Crime Occurence Analysis.gdb\CrimeDT"

arcpy.AddField_management(CrimeDT, "X_Coord", "DOUBLE")
arcpy.AddField_management(CrimeDT, "Y_Coord", "DOUBLE")

with arcpy.da.UpdateCursor(CrimeDT, ["GeographicLocation", "X_Coord", "Y_Coord"]) as cursor:
    for row in cursor:
        row[1] = row[0].split(",")[0]
        row[2] = row[0].split(",")[1]
        row=[i.strip() if i is not None else None for i in row]
        cursor.updateRow(row)

CrimeD_Pts = "crime_points.shp"
spatial_ref = arcpy.SpatialReference(26917)
arcpy.management.XYTableToPoint(CrimeDT, CrimeD_Pts, "X_Coord", "Y_Coord", coordinate_system=spatial_ref)

facility = r"C:\Users\g2panesa\OneDrive - University of Waterloo\Documents\OSM_Data\OSM_Data\shape\points.shp"
facility_20m = "facility_20m.shp"
crime_pts = "crime_points.shp"

arcpy.analysis.Buffer(facility, facility_20m, "20 Meters", dissolve_option="NONE")

arcpy.management.Project(facility_20m,"facility_20m_Proj.shp",26917)

facility_20m_prj = "facility_20m_Proj.shp"

arcpy.analysis.SpatialJoin(facility_20m_prj, crime_pts, "facility_crime_prox.shp", "JOIN_ONE_TO_MANY", "KEEP_COMMON", match_option="INTERSECT")

facility_crime_prox = "facility_crime_prox.shp"

prox_stats = "prox_stats.shp" ##Geotable
arcpy.analysis.Statistics(facility_crime_prox, prox_stats, [["Join_Count","SUM"]], "type")

prox_stats_table = arcpy.da.TableToNumPyArray(prox_stats,"*")

prox_stats_df = pd.DataFrame(prox_stats_table)

print(prox_stats_df)

prox_stats_top_df = prox_stats_df.sort_values(by="SUM_Join_C", ascending=False).head(6)


plt.figure(figsize=(10, 4))
ps_bar_plot = plt.bar(prox_stats_top_df["type"], prox_stats_top_df["SUM_Join_C"], color="green")
plt.bar_label(ps_bar_plot, label_type="edge", fontsize=10)
plt.xticks(rotation=45, ha="right")
plt.show()


