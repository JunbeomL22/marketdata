Option Explicit

Public Sub SaveBondMasterInExcel()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim parameter_date As String
    Dim vrt_bnd_range As String
    Dim bond_master_range As String
    Dim output_file As String
    Dim python_code As String

    ' Set the sheet name
    sheet_name = "BondMaster"
    set ws = ThisWorkbook.Sheets(sheet_name)
    vrt_bnd_range = "VrtBndMaster"
    bond_master_range = "BondMaster"
    parameter_date = ws.range("C2").Value
    output_file = ws.range("C7").Value

    ' Save the bond master in the Excel file
    python_code = "import excel_io;excel_io.save_bond_master_excel("
    python_code = python_code & "parameter_date='" & parameter_date & "',"
    python_code = python_code & "sheet_name='" & sheet_name & "',"
    python_code = python_code & "vrt_bnd_range='" & vrt_bnd_range & "',"
    python_code = python_code & "bond_master_range='" & bond_master_range & "',"
    python_code = python_code & "output_file='" & output_file & "')"

    RunPython python_code
End Sub

Public Sub EraseBondMaster()
    Dim ws As Worksheet
    Dim sheet_name As String
    Dim range_name As String

    sheet_name = "BondMaster"
    range_name = "BondMaster"
    set ws = ThisWorkbook.Sheets("BondMaster")
    ' erase the range from the second rows
    ws.range(range_name).offset(1, 0).resize(ws.range(range_name).rows.count - 1).ClearContents
End Sub
