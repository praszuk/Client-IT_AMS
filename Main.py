from DocumentGenerator import Generator

hardware = [['sdfs', 'jwowowow', 'jsn'], ['wincyj', 'nic caks', 'meh'], ['ok', 'enough', 'xd']]

client = 'askjdla  akski'
middleman = 'asdas asdask'
date_start = '16-10-2018'
date_end = '1-08-2018'

lender_address = 'Bla bla bka B\nasda, Waasasda\n3adad'

if __name__ == '__main__':
    g = Generator()
    g.generate_loan_protocol(client_name=client, middleman_name=middleman, date_start=date_start, date_end=date_end,
                             client_address=lender_address, hardware=hardware)
    g.save_to_file('../demo_modified.docx')
