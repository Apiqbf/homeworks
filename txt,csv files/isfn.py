class Logger:
    def log_action(self,user,action,product,filename):
        ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line=f"{ts},{user._id},{action},{product.id}\n"

        with open(filename,"w",encoding="utf-8")as f:
            f.write(line)

    def read_logs(self,filename):
        self.result=[]

        with open(filename,"r",encoding="utf-8")as f:
            for line in f:
                parts=line.split(",")

                timestamp=parts[0]
                user_id=parts[1]
                action=parts[2]
                product=parts[3]

                self.result.append(
                    {
                        "timestamp":timestamp,
                        "user_id":user_id,
                        "action":action,
                        "product":product
                    }
                )

        return self.result



####10
class OrderIterator:
    def __init__(self,orders):
        self._orders=orders
        self._index=0
    def __iter__(self):
        return self
    def __next__(self):
        if self._index>=len(self._orders):
            raise StopIteration
        order=self._orders[self._index]
        self._index+=1
        return order