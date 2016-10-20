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
        self.folder = sys.argv[3]  # Name of the folder that will have the images, works as label for now
        self.img_type = int(sys.argv[4])  # either 0 for satellite or 1 for street view
        self.path_to_points = sys.argv[5]  # path to points csv

    def get_urls(self, points_csv, img_type):
        """ Creates a list of urls with the csv points """
        size = '500x500'  # Size of imgs, both APIs
        zoom = '20'  # Zoom for satellite API
        heading = '100.78'  # Street view API, where's the camera pointing x axis, 100 is almost straight
        pitch = '-30.90'  # Street view API, where's the camera pointing y axis, -30 points almost to the ground

        with open(points_csv, 'rb') as csv_file:
            f = csv.reader(csv_file, delimiter=',')
            if img_type == 0:  # img_type 0 = satellite view
                return ["http://maps.googleapis.com/maps/api/staticmap?maptype=satellite&center=" +
                        point[0] + "," + point[1] + "&zoom=" + zoom + "&size=" + size +
                        "&key=" + self.gKey for point in f]
            elif img_type == 1:  # img_type 1 = street view
                return ["http://maps.googleapis.com/maps/api/streetview?size=" + size + "&location=" + point[0] +
                        "," + point[1] + "&heading=" + heading + "&pitch=" + pitch + "&key=" +
                        self.svKey for point in f]
            else:
                return []

    def get_dataset(self):
        """ Sends request to Google Maps API and saves result in a PNG file """
        label_folder = os.path.join(os.path.dirname(__file__), self.folder)
        ImgUtils.path_exists(label_folder)

        url_list = self.get_urls(self.path_to_points, self.img_type)
        rs = (grequests.get(u) for u in url_list)

        response_list = grequests.map(rs, size=20, exception_handler=ImgUtils.exception_handler)

        for count, r in enumerate(response_list):
            # TODO The name of the imgs should be changed to some metadata that makes sense...
            if r is not None:
                print(count, r)
                path_to_img = label_folder + '/' + str(count) + ".png"
                with open(path_to_img, 'wb') as outfile:
                    outfile.write(r.content)

if __name__ == "__main__":
    ImgDownload().get_dataset()