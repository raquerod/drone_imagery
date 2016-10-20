import os
import errno
import grequests
import csv
import sys

class ImgUtils(object):

    @staticmethod
    def path_exists(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    @staticmethod
    def exception_handler(request, exception):
        print "Request failed" + str(request) + str(exception)


class ImgDownload(object):

    def __init__(self):
        self.gKey = sys.argv[1]   # Set Google Maps API's secret key from an environment var called gKey
        self.svKey = sys.argv[2]   # Set Google Street View API's secret key
        self.size = '500x500'  # Size of imgs, both APIs
        self.zoom = '20'  # Zoom for satellite API
        self.heading = '100.78'  # Street view API, where's the camera pointing x axis, 100 is almost straight
        self.pitch = '-30.90'  # Street view API, where's the camera pointing y axis, -30 points almost to the ground

    def get_urls(self, points_csv, img_type):
        """ Creates a list of urls with the csv points """
        with open(points_csv, 'rb') as csv_file:
            f = csv.reader(csv_file, delimiter=',')
            if img_type == 0:  # img_type 0 = satellite view
                return ["http://maps.googleapis.com/maps/api/staticmap?maptype=satellite&center=" +
                        point[0] + "," + point[1] + "&zoom=" + self.zoom + "&size=" + self.size +
                        "&key=" + self.gKey for point in f]
            elif img_type == 1:  # img_type 1 = street view
                return ["http://maps.googleapis.com/maps/api/streetview?size=" + self.size + "&location=" + point[0] +
                        "," + point[1] + "&heading=" + self.heading + "&pitch=" + self.pitch + "&key=" +
                        self.svKey for point in f]
            else:
                return []

    def get_dataset(self, path_to_folder, path_to_points, img_type):
        """ Sends request to Google Maps API and saves result in a PNG file """
        url_list = self.get_urls(path_to_points, img_type)
        rs = (grequests.get(u) for u in url_list)

        response_list = grequests.map(rs, size=20, exception_handler=ImgUtils.exception_handler)

        for count, r in enumerate(response_list):
            # TODO The name of the imgs should be changed to some metadata that makes sense...
            if r is not None:
                print(count, r)
                path_to_img = path_to_folder + '/' + str(count) + ".png"
                with open(path_to_img, 'wb') as outfile:
                    outfile.write(r.content)

if __name__ == "__main__":

    label_folder = 'street_view'
    img_type = 1  # img_type = 0 is satellite img =1 is street view
    # label_folder expects the name of the folder in which the img will be stored based on the road classification
    folder = os.path.join(os.path.dirname(__file__), label_folder)
    ImgUtils.path_exists(folder)
    ImgDownload().get_dataset(folder,'points/location_points_neg.csv', img_type)
