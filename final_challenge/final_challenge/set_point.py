# Imports
import rclpy
from rclpy.node import Node
import numpy as np
from std_msgs.msg import Float32
from rcl_interfaces.msg import SetParametersResult

#Class Definition
class SetPointPublisher(Node):
    def __init__(self):
        super().__init__('set_point_node')

        #Parameter Declaration

        # Declarate de parameter 'signal_type' with a default value of sine
        self.declare_parameter('signal_type', 'sine')
        self.declare_parameter('amplitude', 6.0)
        self.declare_parameter('omega', 0.8)
    

        #Retrieve the current parameter value
        self.signal_type = self.get_parameter('signal_type').value
        self.amplitude = self.get_parameter('amplitude').value
        self.omega = self.get_parameter('omega').value

        #Internal parameters
        self.timer_period = 0.05#seconds

        #Create a publisher and timer for the signal
        self.signal_publisher = self.create_publisher(Float32, 'set_point', 10)    ## CHECK FOR THE NAME OF THE TOPIC
        self.amplitude_publisher = self.create_publisher(Float32, 'amplitude', 10)
        self.omega_publisher = self.create_publisher(Float32, 'omega', 10)
        self.timer = self.create_timer(self.timer_period, self.timer_cb)

        
        #Create a messages and variables to be used
        self.signal_msg = Float32()
        self.start_time = self.get_clock().now()

        #Register callback for dynamic parameters
        self.add_on_set_parameters_callback(self.parameter_callback)
        self.get_logger().info("SetPoint Node Started \U0001F680")





    # Timer Callback: Generate and Publish Sine Wave Signal
    def timer_cb(self):
        #Calculate elapsed time
        elapsed_time = (self.get_clock().now() - self.start_time).nanoseconds/1e9

        #Generate signal depending of the type selected
        if self.signal_type == 'sine':
            #Sine Wave
            value = self.amplitude * np.sin(self.omega * elapsed_time)

        elif self.signal_type == 'square':
            #Square Wave
            value = self.amplitude * np.sign(np.sin(self.omega * elapsed_time))

        elif self.signal_type == 'step':
            #Step signal
            value = self.amplitude

        else:
            value = 0.0

        #Asigned computed value to message and publish de signal
        self.signal_msg.data = float(value)
        self.signal_publisher.publish(self.signal_msg)
        amp_msg = Float32()
        amp_msg.data = float(self.amplitude)
        self.amplitude_publisher.publish(amp_msg)

        omega_msg = Float32()
        omega_msg.data = float(self.omega)
        self.omega_publisher.publish(omega_msg)

    #Parameters callback    
    def parameter_callback(self, params):

        for param in params:
            #if the mofified parameter is signal_type
            if param.name == 'signal_type':
                
                #If the selection is not valid, it will show an error
                if param.value not in ['sine', 'square', 'step']:
                    self.get_logger().error("Invalid signal_type")
                    return SetParametersResult(successful=False)

                #Update signal type
                self.signal_type = param.value
                self.get_logger().info(f"Signal changed to: {self.signal_type}")
            elif param.name == 'amplitude':
                self.amplitude = float(param.value)
                self.get_logger().info(f"Amplitude changed to: {self.amplitude}")

            elif param.name == 'omega':
                self.omega = float(param.value)
                self.get_logger().info(f"Omega changed to: {self.omega}")
        return SetParametersResult(successful=True)

    

#Main
def main(args=None):
    rclpy.init(args=args)

    set_point = SetPointPublisher()

    try:
        rclpy.spin(set_point)
    except KeyboardInterrupt:
        pass
    finally:
        set_point.destroy_node()
        rclpy.try_shutdown()

#Execute Node
if __name__ == '__main__':
    main()
