from ua import *
import cv2
import base64
from PIL import Image
from io import BytesIO
import os
import requests

f = open('haarcascade_frontalcatface.xml', 'w')
f.write(requests.get('https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalcatface.xml').content.decode('utf-8'))


def cat_detector_callback(server: UaServer,
                          session_id: UaNodeId,
                          session_context: Void, method_id: UaNodeId, method_context: Void,
                          object_id: UaNodeId,
                          object_context: Void,
                          input_arg: UaList,
                          output_arg: UaList):
    image = Image.open(BytesIO(base64.b64decode(bytes(UaString(input_arg[0].data).value, 'utf-8'))))
    image.save('tmp.jpg')
    image = cv2.imread('tmp.jpg')
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detector = cv2.CascadeClassifier('haarcascade_frontalcatface.xml')
    cat_faces = detector.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=2, minSize=(75, 75))

    for (i, (x, y, w, h)) in enumerate(cat_faces):
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imwrite('result_server.jpg', image)
    with open("result_server.jpg", "rb") as image_file:
        string = UaByteString(base64.b64encode(image_file.read()))
        output_arg[0].data = string

    os.remove('result_server.jpg')
    os.remove('tmp.jpg')
    return UA_STATUSCODES.GOOD


def add_cat_detector_method(server: UaServer):
    input_argument = UaArgument()
    input_argument.description = UaLocalizedText("en-US", "a string")
    input_argument.name = UaString("stringified_cat")
    input_argument.data_type = UA_TYPES.BYTESTRING.type_id
    input_argument.value_rank = UaValueRanks.SCALAR

    output_argument = UaArgument()
    output_argument.description = UaLocalizedText("en-US", "a string")
    output_argument.name = UaString("stringified_cat_detected")
    output_argument.data_type = UA_TYPES.BYTESTRING.type_id
    output_argument.value_rank = UaValueRanks.SCALAR

    cat_attr = UA_ATTRIBUTES_DEFAULT.METHOD
    cat_attr.description = UaLocalizedText("en-US", "detects cats")
    cat_attr.display_name = UaLocalizedText("en-US", "cat detector")
    cat_attr.executable = UaBoolean(True)
    cat_attr.user_executable = UaBoolean(True)
    server.add_method_node(UaNodeId(1, "cat detector"),
                           UA_NS0ID.OBJECTSFOLDER,
                           UA_NS0ID.HASCOMPONENT,
                           UaQualifiedName(1, "cat detector"),
                           cat_detector_callback,
                           input_argument,
                           output_argument, attr=cat_attr)


server = UaServer()
add_cat_detector_method(server)
ret_val = server.run()
