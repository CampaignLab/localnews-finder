import { ReactSearchAutocomplete } from "react-search-autocomplete";
import { constituencies } from "../consts";

let i = 0;

type Item = {
  id: number;
  name: string;
};

const items = constituencies.map((constituency) => {
  return {
    id: i++,
    name: constituency,
  };
});

const Constituency = ({
  className,
  onSelect,
}: {
  className?: string;
  onSelect: (selectedItem: string) => void;
}) => {
  const handleOnSelect = (item: Item) => {
    onSelect(item.name);
  };

  const formatResult = (item: Item) => {
    return (
      <span style={{ display: "block", textAlign: "left" }}>{item.name}</span>
    );
  };

  return (
    <div className={className}>
      <header>
        <div style={{ width: 400 }}>
          <ReactSearchAutocomplete
            items={items}
            onSelect={handleOnSelect}
            autoFocus
            formatResult={formatResult}
          />
        </div>
      </header>
    </div>
  );
};

export default Constituency;
