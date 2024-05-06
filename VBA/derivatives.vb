Option Explicit

Sub SaveDerivativesBaseData()
    Dim ws As Worksheet
    Dim parameter_date As String
    Dim sheet_name as String
    Dim start_date as String
    Dim end_date as String
    Dim drop_spread as String
    Dim file_name as String
    Dim python_code as String

    sheet_name = "DerivativesBase"
    Set ws = ThisWorkbook.Sheets(sheet_name)

    parameter_date = ws.Range("G2").Value
    start_date = ws.Range("G3").Value
    end_date = ws.Range("G4").Value
    if ws.Range("G5").Value = "Y" then
        drop_spread = "True"
    else
        drop_spread = "False"
    end if
    
    file_name = ws.Range("G6").Value

    python_code = "import krx_derivatives;"
    python_code = python_code & "krx_derivatives.save_derivatives_base_data("
    python_code = python_code & "parameter_date='" & parameter_date & "',"
    python_code = python_code & "start_date='" & start_date & "',"
    python_code = python_code & "end_date='" & end_date & "',"
    python_code = python_code & "drop_spread=" & drop_spread & ","
    python_code = python_code & "file_name='" & file_name & "')"

    RunPython python_code
End Sub

Sub LoadDerivativesBaseData()
    Dim ws as Worksheet
    Dim sheet_name as String
    Dim parameter_date as String
    Dim output_head as String
    Dim file_name as String
    Dim python_code as String
    Dim drop_option as String

    sheet_name = "DerivativesBase"
    Set ws = ThisWorkbook.Sheets(sheet_name)

    parameter_date = ws.Range("G2").Value
    file_name = ws.Range("G6").Value
    drop_option = ws.Range("G7").Value
    output_head = ws.Range("G8").Value
    'erase the 1000 rows and 30 columns from output_head
    ws.Range(output_head).Resize(5000, 30).ClearContents

    python_code = "import krx_derivatives;"
    python_code = python_code & "krx_derivatives.load_derivatives_base_data("
    python_code = python_code & "parameter_date='" & parameter_date & "',"
    python_code = python_code & "file_name='" & file_name & "',"
    python_code = python_code & "sheet_name='" & sheet_name & "',"
    python_code = python_code & "output_head='" & output_head & "')"
    
    RunPython python_code
End Sub