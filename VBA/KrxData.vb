Option Explicit

Public Sub SaveKrxEtfBase()
    Dim ws as Worksheet
    Dim parameter_date as String
    Dim file_name as String
    Dim python_code as String

    Set ws = ThisWorkbook.Sheets("BaseData")
    parameter_date = ws.Range("C4").Value
    file_name = ws.Range("C5").Value

    python_code = "import krx_io;krx_io.save_krx_etf_base('" & parameter_date & "', '" & file_name & "')"

    RunPython python_code
End Sub

Public Sub SaveKrxEtfPrice()
    Dim ws as Worksheet
    Dim retrieval_date as String
    Dim parameter_date as String
    Dim file_name as String
    Dim python_code as String

    Set ws = ThisWorkbook.Sheets("BaseData")
    retrieval_date = ws.Range("C3").Value
    parameter_date = ws.Range("C4").Value
    file_name = ws.Range("C6").Value

    python_code = "import krx_io;krx_io.save_krx_etf_price("
    python_code = python_code & "retrieval_date = '" & retrieval_date & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "file_name = '" & file_name & "')"

    RunPython python_code
End Sub

Public Sub SaveKrxStockPrice()
    Dim ws as Worksheet
    Dim retrieval_date as String
    Dim parameter_date as String
    Dim type_name as String
    Dim file_name as String
    Dim python_code as String

    Set ws = ThisWorkbook.Sheets("BaseData")
    retrieval_date = ws.Range("C3").Value
    parameter_date = ws.Range("C4").Value
    file_name = ws.Range("C7").Value
    type_name = ws.Range("C8").Value

    python_code = "import krx_io;krx_io.save_krx_stock_price("
    python_code = python_code & "retrieval_date = '" & retrieval_date & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "type_name = '" & type_name & "',"
    python_code = python_code & "file_name = '" & file_name & "')"

    RunPython python_code
End Sub

Public Sub SaveKrxEtfCombinedBase()
    Dim ws as Worksheet
    Dim parameter_date as String
    Dim base_file as String
    Dim price_file as String
    Dim output_file as String
    Dim python_code as String

    Set ws = ThisWorkbook.Sheets("BaseData")
    parameter_date = ws.Range("C4").Value
    base_file = ws.Range("C5").Value
    price_file = ws.Range("C6").Value
    output_file = ws.Range("C11").Value

    python_code = "import krx_io;krx_io.save_krx_etf_combined_base("
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "base_file = '" & base_file & "',"
    python_code = python_code & "price_file = '" & price_file & "',"
    python_code = python_code & "output_file = '" & output_file & "')"

    RunPython python_code
End Sub


Public Sub LoadKrxEtfCombinedBase()
    Dim ws as Worksheet
    Dim sheet_name as String
    Dim parameter_date as String
    Dim file_name as String
    Dim output_head as String
    Dim python_code as String

    sheet_name = "BaseData"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    parameter_date = ws.Range("C4").Value
    file_name = ws.Range("C11").Value
    output_head = ws.Range("C12").Value

    ws.Range(output_head & "30:" & output_head & "2000").ClearContents

    python_code = "import krx_io;krx_io.load_krx_etf_combined_base("
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "file_name = '" & file_name & "',"
    python_code = python_code & "output_head = '" & output_head & "')"

    RunPython python_code
End Sub

Public Sub SaveKrxAll()
    Call SaveKrxEtfBase
    Call SaveKrxEtfPrice
    Call SaveKrxStockPrice
    Call SaveKrxIndexPrice
    Call SaveKrxEtfCombinedBase
    'Call SaveKrxEtfPdf
End Sub

Public Sub SaveKrxEtfPdf()
    Dim ws as Worksheet
    Dim sheet_name as String
    Dim etf_pdf_add_list_range as String
    Dim parameter_date as String
    Dim combined_base_file as String
    Dim pdf_file as String
    Dim min_cap as Double
    Dim market_type as String
    Dim sleep_time as Double
    Dim python_code as String

    sheet_name = "EtfPdf"
    etf_pdf_add_list_range = "EtfPdfAddList"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    
    parameter_date = ws.Range("C4").Value
    combined_base_file = ws.Range("C5").Value
    pdf_file = ws.Range("C6").Value
    min_cap = ws.Range("C7").Value
    market_type = ws.Range("C8").Value
    sleep_time = ws.Range("C9").Value

    python_code = "import krx_io;krx_io.save_krx_etf_pdf("
    python_code = python_code & "sheet_name = '" & sheet_name & "',"
    python_code = python_code & "etf_pdf_add_list_range = '" & etf_pdf_add_list_range & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "combined_base_file = '" & combined_base_file & "',"
    python_code = python_code & "pdf_file = '" & pdf_file & "',"
    python_code = python_code & "min_cap = " & min_cap & ","
    python_code = python_code & "market_type = '" & market_type & "',"
    python_code = python_code & "sleep_time = " & sleep_time & ")"

    RunPython python_code
End Sub

Public Sub LoadKrxEtfPdf()
    Dim ws as Worksheet
    Dim sheet_name as String
    Dim parameter_date as String
    Dim pdf_file as String
    Dim output_head as String
    Dim python_code as String

    sheet_name = "EtfPdf"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    parameter_date = ws.Range("C4").Value
    pdf_file = ws.Range("C6").Value
    output_head = ws.Range("C10").Value

    ws.Range(output_head & "50:" & output_head & "20000").ClearContents

    python_code = "import krx_io;krx_io.load_krx_etf_pdf("
    python_code = python_code & "sheet_name = '" & sheet_name & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "pdf_file = '" & pdf_file & "',"
    python_code = python_code & "output_head = '" & output_head & "')"

    RunPython python_code
End Sub

Public Sub SaveKrxIndexPrice()
    Dim ws as Worksheet
    Dim retrieval_date as String
    Dim parameter_date as String
    Dim file_name as String
    Dim type_name as String
    Dim python_code as String

    Set ws = ThisWorkbook.Sheets("BaseData")
    retrieval_date = ws.Range("C3").Value
    parameter_date = ws.Range("C4").Value
    file_name = ws.Range("C9").Value
    type_name = ws.Range("C10").Value

    python_code = "import krx_io;krx_io.save_krx_index_price("
    python_code = python_code & "retrieval_date = '" & retrieval_date & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "file_name = '" & file_name & "',"
    python_code = python_code & "type_name = '" & type_name & "')"

    RunPython python_code
End Sub

Public Sub LoadKrxIndexName()
    Dim ws as Worksheet
    Dim sheet_name as String
    Dim parameter_date as String
    Dim file_name as String
    Dim output_head as String
    Dim python_code as String

    sheet_name = "Index"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    parameter_date = ws.Range("C4").Value
    file_name = ws.Range("C5").Value
    output_head = ws.Range("C6").Value

    python_code = "import krx_io;krx_io.load_krx_index_name("
    python_code = python_code & "sheet_name = '" & sheet_name & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "file_name = '" & file_name & "',"
    python_code = python_code & "output_head = '" & output_head & "')"

    RunPython python_code
End Sub

Public Sub SaveKrxDerivativesData()
    Dim ws as Worksheet
    Dim parameter_date as String
    Dim retrieval_date as String
    Dim end_date_cutoff as String
    Dim drop_spread as String
    Dim sleep_time as String
    Dim file_name as String
    Dim python_code as String

    Set ws = ThisWorkbook.Sheets("Derivatives")
    parameter_date = ws.Range("C2").Value
    retrieval_date = ws.Range("C3").Value
    end_date_cutoff = ws.Range("C4").Value
    sleep_time = ws.Range("C6").Value
    file_name = ws.Range("C7").Value

    If ws.Range("C5").Value = "Y" Then
        drop_spread = "True"
    Else
        drop_spread = "False"
    End If

    python_code = "import krx_io;krx_io.save_krx_derivatives_data("
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "retrieval_date = '" & retrieval_date & "',"
    python_code = python_code & "end_date_cutoff = '" & end_date_cutoff & "',"
    python_code = python_code & "drop_spread = " & drop_spread & ","
    python_code = python_code & "sleep_time = " & sleep_time & ","
    python_code = python_code & "file_name = '" & file_name & "')"

    RunPython python_code
End Sub

Public Sub SaveKrxKtbfUnderline()
    Dim ws as Worksheet
    Dim parameter_date as String
    Dim retrieval_date as String
    Dim file_name as String
    Dim python_code as String

    Set ws = ThisWorkbook.Sheets("Derivatives")
    parameter_date = ws.Range("C2").Value
    retrieval_date = ws.Range("C3").Value
    file_name = ws.Range("C8").Value

    python_code = "import krx_io;krx_io.save_krx_ktbf_underline("
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "retrieval_date = '" & retrieval_date & "',"
    python_code = python_code & "file_name = '" & file_name & "')"

    RunPython python_code
End Sub

Public Sub SaveKrxLastTradeTime()
    Dim ws as Worksheet
    Dim parameter_date as String
    Dim retrieval_date as String
    Dim file_name as String
    Dim python_code as String

    Set ws = ThisWorkbook.Sheets("Derivatives")
    parameter_date = ws.Range("C2").Value
    retrieval_date = ws.Range("C3").Value
    file_name = ws.Range("C9").Value

    python_code = "import krx_io;krx_io.save_krx_derivatives_last_trade_time("
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "retrieval_date = '" & retrieval_date & "',"
    python_code = python_code & "file_name = '" & file_name & "')"

    RunPython python_code
End Sub

Public Sub LoadKrxDerivativesData()
    Dim ws as Worksheet
    Dim sheet_name as String
    Dim parameter_date as String
    Dim file_name as String
    Dim output_head as String
    Dim python_code as String

    sheet_name = "Derivatives"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    parameter_date = ws.Range("C2").Value
    file_name = ws.Range("C7").Value
    ouput_head = ws.Range("C11").Value

    ws.Range(output_head & "30:" & output_head & "2000").ClearContents

    python_code = "import krx_io;krx_io.load_krx_derivatives_data("
    python_code = python_code & "sheet_name = '" & sheet_name & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "file_name = '" & file_name & "',"
    python_code = python_code & "output_head = '" & output_head & "')"

    RunPython python_code
End Sub

Public Sub LoadKrxKtbfUnderline()
    Dim ws as Worksheet
    Dim sheet_name as String
    Dim parameter_date as String
    Dim file_name as String
    Dim output_head as String
    Dim python_code as String

    sheet_name = "Derivatives"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    parameter_date = ws.Range("C2").Value
    file_name = ws.Range("C8").Value
    output_head = ws.Range("C12").Value

    python_code = "import krx_io;krx_io.load_krx_ktbf_underline("
    python_code = python_code & "sheet_name = '" & sheet_name & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "file_name = '" & file_name & "',"
    python_code = python_code & "output_head = '" & output_head & "')"

    RunPython python_code
End Sub

Public Sub LoadKrxDerivativesLastTime()
    Dim ws as Worksheet
    Dim sheet_name as String
    Dim parameter_date as String
    Dim file_name as String
    Dim output_head as String
    Dim python_code as String

    sheet_name = "Derivatives"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    parameter_date = ws.Range("C2").Value
    file_name = ws.Range("C9").Value
    output_head = ws.Range("C13").Value

    python_code = "import krx_io;krx_io.load_krx_derivatives_last_trade_time("
    python_code = python_code & "sheet_name = '" & sheet_name & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "file_name = '" & file_name & "',"
    python_code = python_code & "output_head = '" & output_head & "')"

    RunPython python_code
End Sub

Public Sub SaveAllDerivativesInfo()
    Call SaveKrxDerivativesData
    Call SaveKrxKtbfUnderline
    Call SaveKrxLastTradeTime
    Call InfomaxData.SaveInfomaxUnderlineIdentifier
End Sub

Public Sub LoadKrxEtfKtbfBondIsin()
    Dim ws as Worksheet
    Dim sheet_name as String
    Dim parameter_date as String
    Dim file_name as String
    Dim exclude_list as String
    Dum ktbf_und_file as String
    Dim output_head as String
    Dim python_code as String

    sheet_name = "BondMaster"
    Set ws = ThisWorkbook.Sheets(sheet_name)
    parameter_date = ws.Range("C2").Value
    file_name = ws.Range("C3").Value
    exclude_list = ws.Range("C4").Value
    ktbf_und_file = ws.Range("C5").Value
    output_head = ws.Range("C6").Value

    python_code = "import krx_io;krx_io.load_krx_etf_ktbf_bond_isin("
    python_code = python_code & "sheet_name = '" & sheet_name & "',"
    python_code = python_code & "parameter_date = '" & parameter_date & "',"
    python_code = python_code & "file_name = '" & file_name & "',"
    python_code = python_code & "exclude_list = '" & exclude_list & "',"
    python_code = python_code & "ktbf_und_file = '" & ktbf_und_file & "',"
    python_code = python_code & "output_head = '" & output_head & "')"

    RunPython python_code
End Sub



