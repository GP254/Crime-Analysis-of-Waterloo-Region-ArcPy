import arcpy

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


