#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from topic_tools_interfaces.srv import MuxSelect

class DummyMuxSelect(Node):
    def __init__(self):
        super().__init__('dummy_mux_select_node')
        self.srv = self.create_service(MuxSelect, '/mux/select', self.select_callback)
        self.get_logger().info('Dummy /mux/select service is ready to unblock snap!')

    def select_callback(self, request, response):
        self.get_logger().info(f'Received select request for topic: {request.topic}')
        response.success = True
        return response

def main(args=None):
    rclpy.init(args=args)
    node = DummyMuxSelect()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
