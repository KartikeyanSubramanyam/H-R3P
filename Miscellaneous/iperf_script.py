import iperf3
import time
import argparse


def run_iperf_test(server_ip, duration=10, port=5201, retries=3, protocol="tcp"):
    """
    Automates running iperf3 on the client side.

    Args:
        server_ip (str): The IP address of the iperf3 server.
        duration (int): Duration of the iperf3 test in seconds.
        port (int): The port number of the iperf3 server.
        retries (int): Number of retries in case of a failure.
        protocol (str): Protocol to use, either 'tcp' or 'udp'.

    Returns:
        dict: A dictionary containing test results or error details.
    """
    client = iperf3.Client()
    client.server_hostname = server_ip
    client.port = port
    client.duration = duration
    client.protocol = protocol

    for attempt in range(1, retries + 1):
        print(f"Running iperf3 test (Attempt {attempt}/{retries}, Protocol: {protocol.upper()})...")
        try:
            result = client.run()
            if result.error:
                print(f"Error: {result.error}")
            else:
                print(f"Test successful! Bandwidth: {result.sent_Mbps:.2f} Mbps")
                return {
                    "success": True,
                    "protocol": protocol,
                    "bandwidth_Mbps": result.sent_Mbps,
                    "jitter_ms": result.jitter_ms if protocol == "udp" else None,
                    "lost_percent": result.lost_percent if protocol == "udp" else None,
                }
        except Exception as e:
            print(f"Exception occurred: {e}")
        time.sleep(2)  # Delay before retrying

    return {"success": False, "error": "Test failed after multiple attempts."}


def save_results_to_file(filename, results):
    with open(filename, "a") as file:
        file.write("=== Test Results ===\n")
        if results["success"]:
            file.write(f"Protocol: {results['protocol'].upper()}\n")
            file.write(f"Bandwidth: {results['bandwidth_Mbps']:.2f} Mbps\n")
            if results['protocol'] == "udp":
                file.write(f"Jitter: {results['jitter_ms']:.2f} ms\n")
                file.write(f"Packet Loss: {results['lost_percent']:.2f}%\n")
        else:
            file.write(f"Error: {results.get('error', 'Unknown error')}\n")
        file.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate iperf3 client testing.")
    parser.add_argument("--server", type=str, required=True, help="IP address of the iperf3 server.")
    parser.add_argument("--duration", type=int, default=10, help="Test duration in seconds (default: 10).")
    parser.add_argument("--port", type=int, default=5201, help="Port of the iperf3 server (default: 5201).")
    parser.add_argument("--protocol", type=str, choices=["tcp", "udp"], default="tcp", help="Protocol: 'tcp' or 'udp'.")
    parser.add_argument("--output", type=str, default="iperf3_results.txt", help="Output file for results.")
    parser.add_argument("--retries", type=int, default=3, help="Number of retries on failure (default: 3).")
    args = parser.parse_args()
    # Running the script:
    #   Standard TCP test:
    #       python iperf3_client.py --server 10.3.0.5
    #   UDP test:
    #       python iperf3_client.py --server 10.3.0.5 --protocol udp
    #   Custom output file:
    #       python iperf3_client.py --server 10.3.0.5 --output my_results.txt
    print("Starting iperf3 client...")
    results = run_iperf_test(
        server_ip=args.server,
        duration=args.duration,
        port=args.port,
        retries=args.retries,
        protocol=args.protocol,
    )

    save_results_to_file(args.output, results)

    if results["success"]:
        print("\n=== Test Results ===")
        print(f"Protocol: {results['protocol'].upper()}")
        print(f"Bandwidth: {results['bandwidth_Mbps']:.2f} Mbps")
        if results['protocol'] == "udp":
            print(f"Jitter: {results['jitter_ms']:.2f} ms")
            print(f"Packet Loss: {results['lost_percent']:.2f}%")
    else:
        print("\nTest failed.")
        print(f"Error: {results.get('error', 'Unknown error')}")
