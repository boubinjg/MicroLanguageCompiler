begin
if True then
begin
  write("1");
  if not False then
  begin
    write(2);
    if True or False then
    begin
      write(3);
      if not (True or False) then
      begin
        write(4);
        if True or False and False then
        begin
	   write("Here");
	end
      end
    end
  end
end
end
