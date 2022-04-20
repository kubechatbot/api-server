from flask import render_template, request
from . import index_route
from mockup.session import tmp_db, session
import yaml
from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException
from kubernetes.client.api import core_v1_api
from kubernetes.stream import portforward

@index_route.route('/list', methods=['GET'])
def kube_list():
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

def apply_image(blueprint):
    # config.load_kube_config()
    # k8s_client = client.ApiClient()
    # yaml_file = blueprint
    # utils.create_from_dict(k8s_client,yaml_file,verbose=True)
    config.load_kube_config()
    api_instance = core_v1_api.CoreV1Api()
    name = 'hello'
    resp = None
    try:
        resp = api_instance.read_namespaced_pod(name=name,
                                                namespace='default')
    except ApiException as e:
        if e.status != 404:
            print("Unknown error: %s" % e)
            exit(1)

    if not resp:
        print("Pod %s does not exist. Creating it..." % name)
        pod_manifest = blueprint
        api_instance.create_namespaced_pod(body=pod_manifest,
                                           namespace='default')
        while True:
            resp = api_instance.read_namespaced_pod(name=name,
                                                    namespace='default')
            if resp.status.phase != 'Pending':
                break
        print("Done.")

    pf = portforward(
        api_instance.connect_get_namespaced_pod_portforward,
        name, 'default',
        ports='31111',
    )
    http = pf.socket(80)
    http.setblocking(True)
    http.sendall(b'GET / HTTP/1.1\r\n')
    http.sendall(b'Host: 127.0.0.1\r\n')
    http.sendall(b'Connection: close\r\n')
    http.sendall(b'Accept: */*\r\n')
    http.sendall(b'\r\n')
    response = b''
    while True:
        select.select([http], [], [])
        data = http.recv(1024)
        if not data:
            break
        response += data
    http.close()
    print(response.decode('utf-8'))
    error = pf.error(80)
    if error is None:
        print("No port forward errors on port 31111.")
    else:
        print("Port 80 has the following error: %s" % error)

def image_expose():
    with open("resource/svc.yaml") as f:
        yaml_file = yaml.load(f, Loader=yaml.FullLoader)
    config.load_kube_config()
    k8s_client = client.ApiClient()
    utils.create_from_dict(k8s_client,yaml_file,verbose=True)

def delete_pod(podname, namespace):
    config.load_kube_config()
    core_v1 = client.CoreV1Api()
    delete_options = client.V1DeleteOptions()
    try:
        api_response = core_v1.delete_namespaced_pod(podname, namespace, body=delete_options)
        print(api_response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)


@index_route.route('/login', methods=['POST'])
def login_post():
    print(request.form['id'])
    return 'login_post'

@index_route.route('/session', methods=['GET'])
def session_get():
    _ns = request.args.get('namespace', default = 'default', type = str)
    _name = request.args.get('name', default = 'default', type = str)
    
    return str(delete_pod(_name, _ns))

@index_route.route('/session', methods=['POST'])
def session_post():
    with open("resource/layout.yaml") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        cpu = request.form['cpu']
        memory = request.form['memory']
        data['spec']['containers'][0]['resources']['limits']['cpu'] = cpu
        data['spec']['containers'][0]['resources']['limits']['memory'] = memory
        apply_image(data)
    #image_expose()
  
    #kube_list()
    return str(data)



