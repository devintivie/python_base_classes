from time import sleep
from socket_control import socket_control

class iolan_test(socket_control):
    def __init__(self, iAddr, iPort=5025):
        super().__init__(iAddr, iPort)


if __name__ == "__main__":
    test = iolan_test('151.1.10.10', 10002)
    print(test.is_connected)
    ID_COMMAND = 0x2
    WRITE_COMMAND = 0x5
    READ_COMMAND = 0x4

    try:
        test.connect()
        sleep(0.5)
        #Concatenate Address byte
        header = bytearray([0xff, 0xa5])
        write_address = 0x00
        write_data = 100
        # data_packet = bytearray([write_address, write_data])
        data_packet = bytearray()#[write_address, write_data])
        # chassis_address = 1  # might be omitted now
        module_address = 0  # slot address I believe
        
        # address = (chassis_address & 0xf0) + (module_address & 0x0f)
        address = module_address & 0x0f
        length = len(data_packet) + 2 #Length is Data length + 2

        #create full array
        full_array = bytearray(header)
        # full_array.append()
        full_array.append(address)
        full_array.append(length)
        full_array.append(ID_COMMAND)
        # for d in data_packet:
        #     full_array.append(d)
            
        #0x7a
        check_length = length + 1
        check_list = full_array[2:]
        calc_check = sum(check_list)
        check_sum = ~calc_check & 0xff
        print(f'{hex(calc_check)}')
        print(f'{hex(check_sum)}')
        full_array.append(check_sum)

        print(f'{hex(check_sum)}')

        for i in range(4):
            print(f'sent {i+1}')
            resp = test.send_bytes(full_array, delay=0.25, receive=True)
            try:
                for x in resp:
                    print(x)
            except:
                print(resp)

        # print('sent')
        # resp = test.send_bytes(full_array, receive=True)
        # try:
        #     for x in resp:
        #         print(x)
        # except:
        #     print(resp)

        # print('sent')
        # resp = test.send_bytes(full_array, receive=True)
        # try:
        #     for x in resp:
        #         print(x)
        # except:
        #     print(resp)
        # calc_check = aggregate
        print('remainder')
        resp = test.receive()
        try:
            for x in resp:
                print(x)
        except:
            print(resp)

    except Exception as ex:
        print(ex)

        #     //Build List of bytes
        #     var fullArray = new List<byte>(header);
        #     fullArray.Add(address);
        #     fullArray.Add(length);
        #     fullArray.Add(Command);
        #     fullArray.AddRange(Data);

        #     var checkLength = length + 1;       //Checksum bytes count
        #     var checkList = fullArray.GetRange(2, checkLength);     //Copy list of values to new smaller list
        #     var calcCheck = checkList.Aggregate(0, (total, next) => total += next);     //Sum together all values in smaller list of bytes
        #     var checkSum = (byte)~calcCheck;        //checksum = ones complement of summation
        #     fullArray.Add(checkSum);        //Add checksum to end of list
        #     return fullArray.ToArray(); //Convert List to array


        #\x00\xa5\x01\x02\x03\x04\x05\x06\x07\x08\x09", receive=True)

    finally:
        test.close()
        print(test.is_connected)