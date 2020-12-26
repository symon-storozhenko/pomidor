import argparse
import pomidor.pomidor_runner as pr


my_parser = argparse.ArgumentParser(prog='pomidor1.0',
                                    description='pomidor automation')

# Add the arguments
my_parser.add_argument('page_obj', metavar='page_obj', type=str,
                       help='the path to page objects csv file')
my_parser.add_argument('url', type=str, help='main url of the application')
my_parser.add_argument('-b', '--browser', default='Chrome')
my_parser.add_argument('-a', '--additional_urls', type=str)
my_parser.add_argument('-f', '--feature', type=str)

# Execute the parse_args() method
args = my_parser.parse_args()

page_obj = args.page_obj
url = args.url
addtl_urls = args.additional_urls
browser = args.browser
feature = args.feature
nested_dir = 'pomidor_tests'


po = pr.Pomidor(browser, page_obj, url, urls=addtl_urls)
print(vars(args))
if page_obj:
    po.run(nested_dir, feature=feature)
