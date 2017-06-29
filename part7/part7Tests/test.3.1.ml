begin
   int i;
   i := 0;
   while i < 5
   begin
      int j;
      j := 0;
      while j < 5
      begin
         bool x;
         bool y;
         bool z;
         x := (i + j) % 3 == 0;
         y := i % 2 == 0;
         z := j % 2 == 0;
         if x and (y or z) then
         begin
            write(i, " ", j, " ");
         end
         j := j + 1;
      end
      i := i + 1;
   end
end
