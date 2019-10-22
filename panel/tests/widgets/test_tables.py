
try:
    import pandas as pd
except ImportError:
    pass

from bokeh.models.widgets.tables import (
    NumberFormatter, IntEditor, NumberEditor, StringFormatter,
    SelectEditor
)

from panel.widgets import DataFrame


def test_dataframe_widget(dataframe, document, comm):

    table = DataFrame(dataframe)

    model = table.get_root(document, comm)

    index_col, int_col, float_col, str_col = model.columns

    assert index_col.title == 'index'
    assert isinstance(index_col.formatter, NumberFormatter)
    assert isinstance(index_col.editor, IntEditor)

    assert int_col.title == 'int'
    assert isinstance(int_col.formatter, NumberFormatter)
    assert isinstance(int_col.editor, IntEditor)

    assert float_col.title == 'float'
    assert isinstance(float_col.formatter, NumberFormatter)
    assert isinstance(float_col.editor, NumberEditor)

    assert str_col.title == 'str'
    assert isinstance(float_col.formatter, StringFormatter)
    assert isinstance(float_col.editor, NumberEditor)


def test_dataframe_editors(dataframe, document, comm):
    editor = SelectEditor(options=['A', 'B', 'C'])
    table = DataFrame(dataframe, editors={'str': editor})
    model = table.get_root(document, comm)

    assert model.columns[-1].editor is editor

    
def test_dataframe_formatter(dataframe, document, comm):
    formatter = NumberFormatter(format='0.0000')
    table = DataFrame(dataframe, formatters={'float': formatter})
    model = table.get_root(document, comm)
    assert model.columns[2].formatter is formatter


def test_dataframe_triggers(dataframe):
    events = []

    def increment(event, events=events):
        events.append(event)
    
    table = DataFrame(dataframe)
    table.param.watch(increment, 'value')
    table._process_events({'data': {'str': ['C', 'B', 'A']}})
    assert len(events) == 1
    
    
def test_dataframe_does_not_trigger(dataframe):
    events = []

    def increment(event, events=events):
        events.append(event)
    
    table = DataFrame(dataframe)
    table.param.watch(increment, 'value')
    table._process_events({'data': {'str': ['A', 'B', 'C']}})
    assert len(events) == 0


def test_dataframe_selected_dataframe(dataframe):
    table = DataFrame(dataframe, selection=[0, 2])
    pd.testing.assert_frame_equal(dataframe.iloc[[0, 2]], table.selected_dataframe)