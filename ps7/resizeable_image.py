import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self):
        dp = {}
        parent = {}
        for i in range(self.width):
            dp[(i,0)] = self.energy(i,0)
        for j in range(self.height):
            dp[(-1,j)] = float("inf")
            dp[(self.width,j)] = float("inf")
        for j in range(1,self.height):
            for i in range(self.width):
                pixel = (i-1,j-1)
                current = dp[pixel]
                if current > dp[(i,j-1)]:
                    pixel = (i,j-1)
                    current = dp[pixel]
                if current > dp[i+1,j-1]:
                    pixel = (i+1,j-1)
                    current = dp[pixel]
                dp[(i,j)] = current + self.energy(i,j)
                parent[(i,j)] = pixel
        
        pixel = (0,self.height-1)
        value = dp[pixel]
        for i in range(1,self.width):
            if dp[(i,self.height-1)] < value:
                pixel = (i,self.height-1)
                value = dp[pixel]
        
        result = [pixel]
        while pixel in parent:
            pixel = parent[pixel]
            result = [pixel] + result
        
        return result
            
            

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
