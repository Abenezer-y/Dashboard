from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder


##### Functions: Grid functions #####
j_code = JsCode("""
            color: 'red'
            """)

def Grid(df, key, h=690, p =True, jscode=None):

    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_pagination(enabled=p, paginationPageSize=20, paginationAutoPageSize=True)
    gd.configure_default_column(groupable=True, editable=True)
    gd.configure_selection('single')
    grid_option =gd.build()

    if type(jscode) == dict:
        gd.configure_columns("YTD Actual", cellStyle=jscode)

        
    grid = AgGrid(df,  key=key,
                    gridOptions=grid_option,
                    allow_unsafe_jscode=True,
                    update_mode=GridUpdateMode.FILTERING_CHANGED,
                    fit_columns_on_grid_load=True, 
                    reload_data=True,
                    data_return_mode='filtered' ,
                    theme="blue", 
                    height=h)
    return grid
#####################################