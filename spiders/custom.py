from scrapy.exporters import CsvItemExporter


class CsvCustomSeperator(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['encoding'] = 'utf-8'
        kwargs['delimiter'] = '╡'
        super(CsvCustomSeperator, self).__init__(*args, **kwargs)