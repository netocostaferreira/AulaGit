import argparse
import logging
import os
import sys
from db_util import dbchipseq as db
import util.loggerinitializer as utl

# Initialize log object
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
utl.initialize_logger(os.getcwd(), logger)


def main():
    parser = argparse.ArgumentParser(description="A Tool manipulate a sqlite DB")

    subparsers = parser.add_subparsers(title='actions',
                                       description='valid actions',
                                       help='Use sqlite-python.py {action} -h for help with each action',
                                       dest='command'
                                       )

    parser_index = subparsers.add_parser('createdb', help='Create database and tables')

    parser_index.add_argument("--db", dest='db', default=None, action="store", help="The DB name",
                        required=True)

    parser_insert = subparsers.add_parser('insert', help='Insert data on tables')

    parser_insert.add_argument("--file",  default=None, action="store", help="TSV file with the data to be inserted",
                        required=True)

    parser_insert.add_argument("--db", default=None, action="store", help="The DB name",
                        required=True)


    parser_update = subparsers.add_parser('update', help='Update a field in a db')

    parser_update.add_argument("--db", default=None, action="store", help="The DB name",
                        required=True)

    parser_update.add_argument("--assay", default=None, action="store", help="Name of the assay",
                        required=False)

    parser_update.add_argument("--assay_new", default=None, action="store", help="assay_new",
                        required=False)

    parser_update.add_argument("--donor", default=None, action="store", help="Name of the donor",
                               required=False)

    parser_update.add_argument("--donor_new", default=None, action="store", help="Name of the donor",
                               required=False)

    parser_select = subparsers.add_parser('select', help='Select  fields from the db')

    parser_select.add_argument("--db", default=None, action="store", help="The DB name",
                        required=True)

    parser_select.add_argument("--cell_type", default=False, action="store_true", help="Select all cell types",
                        required=False)

    parser_select.add_argument("--assay", default=False, action="store", help="Select all tracks from  assay",
                        required=False)

    parser_select.add_argument("--act", default=False, action="store", help="Select all track name associated with a specific assay_track_name",
                        required=False)



    parser_delete = subparsers.add_parser('delete', help='delete rows from the db')

    parser_delete.add_argument("--tn", default=None, action="store", help="Delete rows where this track_name appears",
                        required=False)

    parser_delete.add_argument("--db", default=None, action="store", help="The DB name",
                        required=True)


    args = parser.parse_args()
    print(args)

    # sys.exit()
    conn = db.connect_db(args.db, logger)

    if args.command == "createdb":

        db.create_table(conn, logger)


    elif args.command == "insert":
        list_of_data = []

        with open(args.file, 'r') as f:
            for line in f:

                # reset dictionary
                line_dict = dict()

                # Skip empty lines
                if line.startswith(','):
                    continue

                # split line
                values = line.strip().split(',')

                # put each field in a dict
                line_dict['cell_type_category'] = values[0]
                line_dict['cell_type'] = values[1]
                line_dict['cell_type_track_name'] = values[2]
                line_dict['cell_type_short'] = values[3]
                line_dict['assay_category'] = values[4]
                line_dict['assay'] = values[5]
                line_dict['assay_track_name'] = values[6]
                line_dict['assay_short'] = values[7]
                line_dict['donor'] = values[8]
                line_dict['time_point'] = values[9]
                line_dict['view'] = values[10]
                line_dict['track_name'] = values[11]
                line_dict['track_type'] = values[12]
                line_dict['track_density'] = values[13]
                line_dict['provider_institution'] = values[14]
                line_dict['source_server'] = values[15]
                line_dict['source_path_to_file'] = values[16]
                line_dict['server'] = values[17]
                line_dict['path_to_file'] = values[18]
                line_dict['new_file_name'] = values[19]


                #append the dict to a list
                list_of_data.append(line_dict)

        db.insert_data(conn, list_of_data, logger)


    elif args.command == "update" and args.assay is not None:
        db.update_assay(conn, args.assay, args.assay_new, logger)

    elif args.command == "update" and args.donor is not None:
        db.update_donor(conn, args.donor, args.donor_new, logger)


    elif args.command == "select" and args.cell_type is not False:
        all_cell_types = db.select_cell_types(conn, logger)

        for i in all_cell_types:
            print(i[0])


    elif args.command == "select" and args.assay is not False:

        all_tracks_assay = db.select_tracks_assay(conn, args.assay, logger)
        print("\n| track_name\t| track_type\t| track_density")
        for i in all_tracks_assay:
            print("|","\t| ".join(i))


    elif args.command == "select" and args.act is not False:
        all_cell_type = db.select_assay_cell_type(conn, args.act, logger)

        print("\n| Track_name")
        for i in all_cell_type:
            print(i[0])

    elif args.command == "select" and args.act is not False:
        all_assay_cell_type = db.select_assay_cell_type(conn, args.act, logger)

        print("\n| cell_type")
        for i in all_assay_cell_type:
            print(i)


    elif args.command == "delete":
        db.delete_track_name(conn, args.tn, logger)


if __name__ == '__main__':
    main()




